#!/usr/bin/env python3
"""Run the repository-locked Spec Kit without a user-installed specify CLI."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]


def command(root, uv, args, *, setup=False):
    project = root / "tools/ai/spec-kit"
    if setup:
        return [uv, "sync", "--locked", "--no-dev", "--project", str(project)]
    binary = project / ".venv" / ("Scripts/specify.exe" if os.name == "nt" else "bin/specify")
    return [uv, "run", "--locked", "--no-dev", "--project", str(project), "--", str(binary), *args]


def check_agents(root):
    expected = {"spec_author", "spec_planner", "spec_implementer", "spec_reviewer",
                "spec_verifier", "security_reviewer", "stack_advisor"}
    directory = root / ".codex/agents"
    paths = {directory / (name + ".toml") for name in expected}
    paths.update(directory.glob("*.toml"))
    names = set()
    for path in sorted(paths):
        data = tomllib.loads(path.read_text())
        for field in ("name", "description", "developer_instructions"):
            value = data.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"invalid agent field: {path.name}: {field}")
        name = data["name"]
        if name != path.stem or name in names:
            raise ValueError(f"invalid or duplicate agent name: {path.name}")
        names.add(name)
    if not (root / ".agents/skills/project-sdd/SKILL.md").is_file():
        raise ValueError("missing project-sdd entry skill")


def main(args=None):
    args = list(sys.argv[1:] if args is None else args)
    if not args:
        print("Usage: python3 scripts/ai/specify.py setup|doctor|<Spec Kit CLI arguments>")
        return 0
    uv = shutil.which("uv")
    if not uv:
        print("uv is required. Install uv using https://docs.astral.sh/uv/getting-started/installation/", file=sys.stderr)
        return 1
    env = dict(os.environ)
    # Never select a caller's active venv or an unrelated project's environment.
    env.pop("VIRTUAL_ENV", None)
    env["UV_PROJECT_ENVIRONMENT"] = str(ROOT / "tools/ai/spec-kit/.venv")
    try:
        if args == ["setup"]:
            subprocess.run(command(ROOT, uv, [], setup=True), cwd=ROOT, env=env, check=True)
            args = ["doctor"]
        if args == ["doctor"]:
            check_agents(ROOT)
            args = ["integration", "status", "--json"]
        result = subprocess.run(command(ROOT, uv, args), cwd=ROOT, env=env)
        return result.returncode
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Spec harness failed: {type(error).__name__}; check uv, lockfile and project agent files.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
