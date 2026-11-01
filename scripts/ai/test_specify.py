"""Portable launcher invariants; fresh-checkout integration is checked separately."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import specify


class SpecHarnessTests(unittest.TestCase):
    def test_cli_always_targets_project_binary_including_korean_spaces(self):
        with tempfile.TemporaryDirectory(prefix="루이 푸리 ") as name:
            root = Path(name)
            argv = specify.command(root, "/uv", ["version"])
            target = Path(argv[-2])
            self.assertTrue(target.is_relative_to(root / "tools/ai/spec-kit/.venv"))
            self.assertNotEqual(argv[-2], "specify")
            self.assertIn("--locked", argv)
            self.assertEqual(argv[-1], "version")

    def test_missing_uv_fails_without_using_global_specify(self):
        with patch.object(specify.shutil, "which", return_value=None), \
                patch.object(specify.subprocess, "run") as run, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(specify.main(["version"]), 1)
            run.assert_not_called()

    def test_callers_virtualenv_is_never_reused(self):
        with patch.object(specify.shutil, "which", return_value="/uv"), \
                patch.object(specify.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run, \
                patch.dict(specify.os.environ, {"VIRTUAL_ENV": "/other", "UV_PROJECT_ENVIRONMENT": "/other"}):
            self.assertEqual(specify.main(["version"]), 0)
            env = run.call_args.kwargs["env"]
            self.assertNotIn("VIRTUAL_ENV", env)
            self.assertEqual(Path(env["UV_PROJECT_ENVIRONMENT"]), specify.ROOT / "tools/ai/spec-kit/.venv")

    def test_upstream_failure_propagates_without_fallback(self):
        with patch.object(specify.shutil, "which", return_value="/uv"), \
                patch.object(specify.subprocess, "run", return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(specify.main(["version"]), 7)
            self.assertEqual(run.call_count, 1)

    def test_project_roles_have_valid_native_fields(self):
        specify.check_agents(specify.ROOT)

    def test_missing_role_is_not_reported_ready(self):
        with tempfile.TemporaryDirectory() as name, self.assertRaises(OSError):
            specify.check_agents(Path(name))

    def test_cli_version_and_source_are_locked_to_project_metadata(self):
        root = specify.ROOT / "tools/ai/spec-kit"
        project = tomllib.loads((root / "pyproject.toml").read_text())
        lock = tomllib.loads((root / "uv.lock").read_text())
        package = next(p for p in lock["package"] if p["name"] == "specify-cli")
        integration = json.loads((specify.ROOT / ".specify/integration.json").read_text())
        self.assertIn("specify-cli==" + package["version"], project["project"]["dependencies"])
        self.assertEqual(package["version"], integration["version"])
        self.assertIn(project["tool"]["uv"]["sources"]["specify-cli"]["rev"], package["source"]["git"])

    def test_local_runtime_is_ignored_but_role_and_lock_are_shareable(self):
        paths = ["tools/ai/spec-kit/.venv/pyvenv.cfg"]
        ignored = subprocess.check_output(["git", "-C", str(specify.ROOT), "check-ignore", "--no-index", *paths], text=True)
        self.assertEqual(ignored.strip(), paths[0])
        result = subprocess.run(["git", "-C", str(specify.ROOT), "check-ignore", "--no-index",
                                 "tools/ai/spec-kit/uv.lock", ".codex/agents/spec_author.toml",
                                 ".agents/skills/project-sdd/SKILL.md"], capture_output=True)
        self.assertEqual(result.returncode, 1)


class AgentReadinessTests(unittest.TestCase):
    # Keep the acceptance fixture independent of the implementation's role list.
    roles = ("spec_author", "spec_planner", "spec_implementer", "spec_reviewer",
             "spec_verifier", "security_reviewer", "stack_advisor")
    fields = ("name", "description", "developer_instructions")

    @contextlib.contextmanager
    def project(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for role in self.roles:
                self.write_role(root, role)
            skill = root / ".agents/skills/project-sdd/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("entry skill")
            yield root

    def write_role(self, root, role, **changes):
        data = dict(name=role, description="Role description", developer_instructions="Role instructions")
        data.update(changes)
        path = root / ".codex/agents" / (role + ".toml")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(key + " = " + json.dumps(value)
                                  for key, value in data.items() if value is not None))
        return path

    def test_c01_normal_seven_roles(self):
        with self.project() as root:
            specify.check_agents(root)

    def test_c02_valid_additional_role(self):
        with self.project() as root:
            self.write_role(root, "extra_role")
            specify.check_agents(root)

    def test_c03_each_required_role_is_required(self):
        for role in self.roles:
            with self.subTest(role=role), self.project() as root:
                (root / ".codex/agents" / (role + ".toml")).unlink()
                with self.assertRaises(OSError):
                    specify.check_agents(root)

    def test_c04_each_field_is_required(self):
        for field in self.fields:
            with self.subTest(field=field), self.project() as root:
                self.write_role(root, "spec_author", **{field: None})
                with self.assertRaises(ValueError):
                    specify.check_agents(root)

    def test_c05_empty_and_whitespace_fields_are_rejected(self):
        for field in self.fields:
            for value in ("", "   ", "\t\n"):
                with self.subTest(field=field, value=value), self.project() as root:
                    self.write_role(root, "spec_author", **{field: value})
                    with self.assertRaises(ValueError):
                        specify.check_agents(root)

    def test_c06_nonstring_fields_are_rejected(self):
        for field in self.fields:
            for literal in ("0", "7", "false", "true", "[]", "[1]", "{}", "{ key = 1 }"):
                with self.subTest(field=field, literal=literal), self.project() as root:
                    path = self.write_role(root, "spec_author")
                    lines = path.read_text().splitlines()
                    path.write_text("\n".join(field + " = " + literal if line.startswith(field + " = ") else line
                                              for line in lines))
                    with self.assertRaises(ValueError):
                        specify.check_agents(root)

    def test_c07_nonempty_content_may_have_surrounding_whitespace(self):
        for field in ("description", "developer_instructions"):
            with self.subTest(field=field), self.project() as root:
                self.write_role(root, "spec_author", **{field: " \tContent\n "})
                specify.check_agents(root)

    def test_c08_names_must_match_filename_exactly(self):
        for value in ("other", " spec_author", "spec_author "):
            with self.subTest(value=value), self.project() as root:
                self.write_role(root, "spec_author", name=value)
                with self.assertRaises(ValueError):
                    specify.check_agents(root)

    def test_c09_additional_role_cannot_duplicate_name(self):
        with self.project() as root:
            self.write_role(root, "extra_role", name="spec_author")
            with self.assertRaises(ValueError):
                specify.check_agents(root)

    def test_c10_additional_roles_follow_same_contract(self):
        for change in ({"description": " "}, {"developer_instructions": True}, {"name": "other"}):
            with self.subTest(change=change), self.project() as root:
                self.write_role(root, "extra_role", **change)
                with self.assertRaises(ValueError):
                    specify.check_agents(root)

    def test_c11_malformed_toml_is_rejected(self):
        with self.project() as root:
            (root / ".codex/agents/spec_author.toml").write_text("name = [")
            with self.assertRaises(ValueError):
                specify.check_agents(root)

    def test_c12_role_directory_is_rejected(self):
        with self.project() as root:
            path = root / ".codex/agents/spec_author.toml"
            path.unlink()
            path.mkdir()
            with self.assertRaises(OSError):
                specify.check_agents(root)

    def test_c13_read_error_is_not_reported_ready(self):
        with self.project() as root:
            path = root / ".codex/agents/spec_author.toml"
            read_text = Path.read_text

            def read(current, *args, **kwargs):
                if current == path:
                    raise PermissionError("synthetic read failure")
                return read_text(current, *args, **kwargs)

            with patch.object(Path, "read_text", read), self.assertRaises(OSError):
                specify.check_agents(root)


    def test_c14_missing_entry_skill_is_rejected(self):
        with self.project() as root:
            (root / ".agents/skills/project-sdd/SKILL.md").unlink()
            with self.assertRaises(ValueError):
                specify.check_agents(root)

    def test_c15_entry_skill_directory_is_rejected(self):
        with self.project() as root:
            path = root / ".agents/skills/project-sdd/SKILL.md"
            path.unlink()
            path.mkdir()
            with self.assertRaises(ValueError):
                specify.check_agents(root)

    def test_c16_invalid_role_stops_doctor_before_upstream(self):
        with self.project() as root:
            self.write_role(root, "spec_author", description="   ")
            with patch.object(specify, "ROOT", root), \
                    patch.object(specify.shutil, "which", return_value="/uv"), \
                    patch.object(specify.subprocess, "run") as run, \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(specify.main(["doctor"]), 1)
                run.assert_not_called()

    def test_c17_missing_skill_stops_doctor_before_upstream(self):
        with self.project() as root:
            (root / ".agents/skills/project-sdd/SKILL.md").unlink()
            with patch.object(specify, "ROOT", root), \
                    patch.object(specify.shutil, "which", return_value="/uv"), \
                    patch.object(specify.subprocess, "run") as run, \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(specify.main(["doctor"]), 1)
                run.assert_not_called()

    def test_c18_c19_valid_doctor_preserves_upstream_command_and_result(self):
        for returncode in (0, 7):
            with self.subTest(returncode=returncode), self.project() as root:
                with patch.object(specify, "ROOT", root), \
                        patch.object(specify.shutil, "which", return_value="/uv"), \
                        patch.object(specify.subprocess, "run",
                                     return_value=subprocess.CompletedProcess([], returncode)) as run, \
                        patch.dict(specify.os.environ, {"VIRTUAL_ENV": "/other", "UV_PROJECT_ENVIRONMENT": "/other"}):
                    self.assertEqual(specify.main(["doctor"]), returncode)
                    run.assert_called_once()
                    binary = root / "tools/ai/spec-kit/.venv" / (
                        "Scripts/specify.exe" if specify.os.name == "nt" else "bin/specify")
                    self.assertEqual(run.call_args.args[0], [
                        "/uv", "run", "--locked", "--no-dev", "--project", str(root / "tools/ai/spec-kit"),
                        "--", str(binary), "integration", "status", "--json"])
                    self.assertEqual(run.call_args.kwargs["cwd"], root)
                    env = run.call_args.kwargs["env"]
                    self.assertNotIn("VIRTUAL_ENV", env)
                    self.assertEqual(env["UV_PROJECT_ENVIRONMENT"], str(root / "tools/ai/spec-kit/.venv"))
