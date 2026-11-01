"""Local human review checkpoints; not an identity or tool-execution sandbox."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GATES = ("issue", "plan", "pr")


class GateError(ValueError):
    pass


def state_path(root, task):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", task):
        raise GateError("task ID must use letters, digits, hyphens or underscores")
    path = root / ".codex/local/gates" / (task + ".json")
    if not path.resolve().is_relative_to(root.resolve()):
        raise GateError("gate state must remain inside the project")
    return path


def load(root, task):
    path = state_path(root, task)
    if not path.exists():
        return {"version": 1, "task": task, "gates": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if state["version"] != 1 or state["task"] != task or not isinstance(state["gates"], dict):
            raise ValueError("invalid state")
        return state
    except (ValueError, KeyError, TypeError) as error:
        raise GateError("invalid gate state; stop for human inspection") from error


def save(root, task, state):
    path = state_path(root, task)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False) as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def documents(root, names):
    if not names:
        raise GateError("review documents are required")
    result = {}
    for name in names:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise GateError("review document must be an existing project file: " + name)
        data = path.read_bytes()
        if not data.strip():
            raise GateError("review document is empty: " + name)
        result[path.relative_to(root.resolve()).as_posix()] = hashlib.sha256(data).hexdigest()
    return dict(sorted(result.items()))


def git(root, *args):
    try:
        return subprocess.check_output(["git", "-C", str(root), *args],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise GateError("PR gate requires a real committed Git checkout") from error


def pr_head(root):
    head = git(root, "rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40,64}", head):
        raise GateError("invalid Git HEAD")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise GateError("PR review requires a clean checkout; commit/push only when authorized")
    return head


def require(root, state, gate, decisions=("approved",)):
    entry = state["gates"].get(gate)
    if not isinstance(entry, dict):
        raise GateError(gate + ": not submitted; stop")
    if gate != "issue":
        require(root, state, "issue")
    if gate == "pr":
        require(root, state, "plan")
    if documents(root, entry["files"]) != entry["files"]:
        raise GateError(gate + ": documents changed; resubmit and obtain human review again")
    if gate == "pr" and pr_head(root) != entry["head"]:
        raise GateError("pr: HEAD changed; resubmit and obtain human review again")
    if entry.get("decision") not in decisions:
        raise GateError(gate + ": human decision required; stop")
    return entry


def submit(root, task, gate, files, url=None):
    state = load(root, task)
    if gate != "issue":
        require(root, state, "issue")
    if gate == "pr":
        require(root, state, "plan")
        if not url or not re.fullmatch(r"https://[^/\s]+/[^/\s]+/[^/\s]+/pull/[1-9][0-9]*", url):
            raise GateError("a real PR URL is required")
    if gate == "plan" and not {"spec.md", "plan.md", "tasks.md"}.issubset(
            {Path(name).name for name in files}):
        raise GateError("plan review must include spec.md, plan.md and tasks.md plus linked design documents")
    entry = {"files": documents(root, files), "decision": "pending"}
    if gate == "pr":
        entry.update(head=pr_head(root), url=url)
    entry["digest"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    # Resubmission always revokes this gate and every downstream decision.
    for downstream in GATES[GATES.index(gate):]:
        state["gates"].pop(downstream, None)
    state["gates"][gate] = entry
    save(root, task, state)
    return entry


def decide(root, task, gate, decision, reviewer, stdin=None, stdout=None):
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    # Prevent accidental automation/piped approval; a TTY is not human identity proof.
    if not stdin.isatty() or not stdout.isatty():
        raise GateError("human-only command: use your own interactive terminal; piped approval rejected")
    if not reviewer.strip():
        raise GateError("reviewer name is required")
    state = load(root, task)
    entry = require(root, state, gate, ("pending", "changes_requested", "approved"))
    if decision == "changes_requested" and gate != "pr":
        raise GateError("revise issue/plan and resubmit instead")
    token = f"{decision} {task} {gate} {entry['digest']}"
    print(json.dumps(entry, ensure_ascii=False, indent=2), file=stdout)
    print("Read every listed document and the PR code. Type exactly: " + token, file=stdout)
    stdout.flush()
    if stdin.readline().strip() != token:
        raise GateError("confirmation did not match; approval not recorded")
    # Close changes made while the human was reviewing the displayed revision.
    current = load(root, task)
    latest = require(root, current, gate, ("pending", "changes_requested", "approved"))
    if latest != entry:
        raise GateError("submission changed during review; review the new submission")
    latest.update(decision=decision, reviewer=reviewer.strip(),
                  reviewed_at=datetime.now(timezone.utc).isoformat())
    save(root, task, current)
    return latest


def check(root, task, stage):
    if stage == "merge":
        raise GateError("merge is human-only; agents must never merge, enable auto-merge or join a merge queue")
    state = load(root, task)
    require(root, state, "issue")
    if stage in ("implement", "pr-open", "review-fix", "handoff-merge"):
        require(root, state, "plan")
    if stage == "review-fix":
        require(root, state, "pr", ("changes_requested",))
    if stage == "handoff-merge":
        require(root, state, "pr")
    return {"task": task, "stage": stage, "allowed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("submit", "decide", "check", "status"):
        command = commands.add_parser(name)
        command.add_argument("task")
        if name in ("submit", "decide"):
            command.add_argument("gate", choices=GATES)
        if name == "submit":
            command.add_argument("--files", nargs="+", required=True)
            command.add_argument("--url")
        if name == "decide":
            command.add_argument("decision", choices=("approved", "changes_requested"))
            command.add_argument("--reviewer", required=True)
        if name == "check":
            command.add_argument("stage", choices=("specify", "plan", "implement", "pr-open",
                                                    "review-fix", "handoff-merge", "merge"))
    args = parser.parse_args()
    try:
        if args.command == "submit":
            result = submit(ROOT, args.task, args.gate, args.files, args.url)
        elif args.command == "decide":
            result = decide(ROOT, args.task, args.gate, args.decision, args.reviewer)
        elif args.command == "check":
            result = check(ROOT, args.task, args.stage)
        else:
            result = load(ROOT, args.task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (GateError, OSError, KeyError, TypeError) as error:
        print("BLOCKED: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
