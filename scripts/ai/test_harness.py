"""Behavior tests in disposable roots; no real Codex event/trust is simulated."""
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import harness


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="루이 푸리 ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def event(self, name="SessionStart", session="one"):
        return {"hook_event_name": name, "session_id": session, "cwd": str(self.root)}

    def payload(self):
        return {name: "미실행 또는 해당 없음" for name in harness.FIELDS} | {
            "task_id": "test-handoff", "goal": "검증된 인계를 저장",
            "next_step": "현재 Git 상태부터 재확인", "links": "docs/ai/memory/INDEX.md"}

    def test_start_has_small_pointers_without_transcript_or_secret(self):
        event = self.event() | {"transcript_path": "/not-readable", "tool_input": "PRIVATE-CONTENT"}
        result = harness.handle_hook(self.root, event)
        text = json.dumps(result, ensure_ascii=False)
        self.assertLess(len(text.encode()), 2048)
        self.assertIn("docs/ai/ROUTING.md", text)
        for path in (self.root / ".codex/local").rglob("*.json"):
            record = path.read_text()
            self.assertNotIn("PRIVATE-CONTENT", record)
            self.assertNotIn("not-readable", record)

    def test_compact_saves_only_mechanical_state_without_blocking(self):
        result = harness.handle_hook(self.root, self.event("PreCompact"))
        self.assertNotIn("decision", result)
        self.assertNotIn("continue", result)
        record = next((self.root / ".codex/local/state").rglob("*.json"))
        self.assertEqual(json.loads(record.read_text())["event"], "PreCompact")
        self.assertFalse((self.root / ".codex/local/sessions").exists())

    def test_unknown_event_rejected_without_state(self):
        with self.assertRaises(ValueError):
            harness.handle_hook(self.root, self.event("PreToolUse"))
        self.assertFalse((self.root / ".codex").exists())

    def test_foreign_cwd_rejected(self):
        with self.assertRaises(ValueError):
            harness.handle_hook(self.root, self.event() | {"cwd": str(self.root.parent)})

    def test_relative_cwd_rejected(self):
        with self.assertRaises(ValueError):
            harness.handle_hook(self.root, self.event() | {"cwd": "."})

    def test_bad_session_ids_rejected(self):
        for value in (None, "", " ", 4, "x" * 257):
            with self.subTest(value=type(value).__name__), self.assertRaises(ValueError):
                harness.handle_hook(self.root, self.event(session=value))

    def test_session_id_is_not_a_path_or_shell_command(self):
        value = "../../$(touch NEVER_EXECUTE); 보안"
        harness.handle_hook(self.root, self.event(session=value))
        dirs = list((self.root / ".codex/local/state").iterdir())
        self.assertEqual(dirs[0].name, harness.session_key(value))
        self.assertFalse((self.root / "NEVER_EXECUTE").exists())

    def test_concurrent_calls_never_overwrite_same_session(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(lambda _: harness.handle_hook(self.root, self.event()), range(18)))
        records = list((self.root / ".codex/local/state").rglob("*.json"))
        self.assertEqual(len(records), 18)
        self.assertTrue(all(json.loads(p.read_text())["event"] == "SessionStart" for p in records))
        self.assertEqual(list((self.root / ".codex/local").rglob(".tmp-*")), [])

    def test_sessions_do_not_load_each_others_handoff(self):
        path = harness.save_handoff(self.root, "first", self.payload())
        result = harness.handle_hook(self.root, self.event(session="second"))
        text = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(path.name, text)
        result = harness.handle_hook(self.root, self.event(session="first"))
        self.assertIn(path.name, json.dumps(result))

    def test_handoff_roundtrip_is_unique_and_complete(self):
        paths = [harness.save_handoff(self.root, "first", self.payload()) for _ in range(2)]
        self.assertNotEqual(*paths)
        for path in paths:
            data = json.loads(path.read_text())
            self.assertEqual(data["next_step"], "현재 Git 상태부터 재확인")
            self.assertIn("head", data["git"])
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_incomplete_handoff_does_not_publish_file(self):
        payload = self.payload()
        del payload["limits"]
        with self.assertRaises(ValueError):
            harness.save_handoff(self.root, "first", payload)
        self.assertFalse((self.root / ".codex").exists())

    def test_symlinked_state_directory_is_rejected(self):
        (self.root / "other").mkdir()
        (self.root / ".codex").symlink_to(self.root / "other", target_is_directory=True)
        with self.assertRaises(ValueError):
            harness.handle_hook(self.root, self.event())
        self.assertEqual(list((self.root / "other").iterdir()), [])

    def test_input_limits_and_malformed_json(self):
        for value in (b"{", b"[]", b" " * (harness.MAX_INPUT + 1)):
            with self.subTest(size=len(value)), self.assertRaises(ValueError):
                harness.read_object(io.BytesIO(value))

    def test_registered_command_from_root_and_nested_korean_directory(self):
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True, capture_output=True)
        script_dir = self.root / "scripts/ai"
        script_dir.mkdir(parents=True)
        shutil.copy(harness.ROOT / "scripts/ai/harness.py", script_dir / "harness.py")
        nested = self.root / "하위 폴더"
        nested.mkdir()
        config = json.loads((harness.ROOT / ".codex/hooks.json").read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        for cwd in (self.root, nested):
            event = self.event() | {"cwd": str(cwd)}
            result = subprocess.run(["/bin/sh", "-c", command], cwd=cwd,
                                    input=json.dumps(event), capture_output=True,
                                    text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("hookSpecificOutput", json.loads(result.stdout))

    def test_registered_hook_ignores_nested_shadow_script(self):
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True, capture_output=True)
        scripts = self.root / "scripts/ai"
        scripts.mkdir(parents=True)
        shutil.copy(harness.ROOT / "scripts/ai/harness.py", scripts / "harness.py")
        nested = self.root / "generated"
        shadow = nested / "scripts/ai"
        shadow.mkdir(parents=True)
        marker = nested / "shadow-executed"
        (shadow / "harness.py").write_text(
            "from pathlib import Path\nPath(__file__).parents[2].joinpath('shadow-executed').touch()\n")
        config = json.loads((harness.ROOT / ".codex/hooks.json").read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        result = subprocess.run(["/bin/sh", "-c", command], cwd=nested,
                                input=json.dumps(self.event() | {"cwd": str(nested)}),
                                capture_output=True, text=True, timeout=5)
        self.assertFalse(marker.exists(), "nested script must not execute as project hook")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hookSpecificOutput", json.loads(result.stdout))

    def test_hook_launcher_ignores_inherited_git_location(self):
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True, capture_output=True)
        scripts = self.root / "scripts/ai"
        scripts.mkdir(parents=True)
        shutil.copy(harness.ROOT / "scripts/ai/harness.py", scripts / "harness.py")
        other = self.root / "other"
        other.mkdir()
        subprocess.run(["git", "-C", str(other), "init", "-q"], check=True, capture_output=True)
        config = json.loads((harness.ROOT / ".codex/hooks.json").read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        env = dict(os.environ, GIT_DIR=str(other / ".git"), GIT_WORK_TREE=str(other))
        result = subprocess.run(["/bin/sh", "-c", command], cwd=self.root, env=env,
                                input=json.dumps(self.event()), capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hookSpecificOutput", json.loads(result.stdout))

    def test_cli_error_never_echoes_input(self):
        result = subprocess.run([sys.executable, "-B", str(harness.ROOT / "scripts/ai/harness.py"), "hook"],
                                input="PRIVATE-INVALID-JSON", text=True, capture_output=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("PRIVATE-INVALID-JSON", result.stderr)

    def test_sensitive_artifacts_are_ignored_and_config_is_shared(self):
        paths = [".codex/local/sessions/a.json", ".codex/local/state/a.json",
                 ".playwright-cli/auth.json", ".playwright/.auth/user.json", ".env.local",
                 "tools/ai/node_modules/file", "test-results/trace.zip"]
        result = subprocess.run(["git", "-C", str(harness.ROOT), "check-ignore", "--no-index", *paths],
                                text=True, capture_output=True, timeout=5, check=True)
        self.assertEqual(set(result.stdout.splitlines()), set(paths))
        result = subprocess.run(["git", "-C", str(harness.ROOT), "check-ignore", "--no-index",
                                 ".codex/hooks.json", ".codex/config.toml", "tools/ai/package-lock.json"],
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
