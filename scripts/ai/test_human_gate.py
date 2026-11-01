"""Expected workflow boundaries, including stale approvals and review cycles."""
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import human_gate as gate


class HumanGateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="휴먼 게이트 ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.task = "PET-001"
        for name in ("issue.md", "spec.md", "plan.md", "tasks.md", "pr.md"):
            (self.root / name).write_text("# Review " + name, encoding="utf-8")

    def submit(self, name):
        files = {"issue": ["issue.md"], "plan": ["spec.md", "plan.md", "tasks.md"],
                 "pr": ["pr.md"]}[name]
        return gate.submit(self.root, self.task, name, files,
                           "https://github.com/example/pets/pull/1" if name == "pr" else None)

    def human(self, name, decision="approved"):
        entry = gate.load(self.root, self.task)["gates"][name]
        incoming = io.StringIO(f"{decision} {self.task} {name} {entry['digest']}\n")
        outgoing = io.StringIO()
        incoming.isatty = lambda: True
        outgoing.isatty = lambda: True
        return gate.decide(self.root, self.task, name, decision, "fixture human", incoming, outgoing)

    def approved_plan(self):
        self.submit("issue")
        self.human("issue")
        self.submit("plan")
        self.human("plan")

    def real_git(self):
        def run(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True,
                           capture_output=True)
        run("init", "-q")
        (self.root / ".gitignore").write_text(".codex/local/\n")
        run("add", ".")
        run("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-qm", "isolated fixture")
        return run

    def test_missing_issue_blocks_specification(self):
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "specify")

    def test_pending_issue_blocks_planning_and_plan_submission(self):
        self.submit("issue")
        for action in (lambda: gate.check(self.root, self.task, "plan"), lambda: self.submit("plan")):
            with self.subTest(action=action), self.assertRaises(gate.GateError):
                action()

    def test_issue_approval_allows_specification_but_not_implementation(self):
        self.submit("issue")
        self.human("issue")
        self.assertTrue(gate.check(self.root, self.task, "specify")["allowed"])
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "implement")

    def test_pending_plan_blocks_implementation(self):
        self.submit("issue")
        self.human("issue")
        self.submit("plan")
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "implement")

    def test_incomplete_plan_bundle_is_not_submitted(self):
        self.submit("issue")
        self.human("issue")
        for missing in ("spec.md", "plan.md", "tasks.md"):
            files = [name for name in ("spec.md", "plan.md", "tasks.md") if name != missing]
            with self.subTest(missing=missing), self.assertRaises(gate.GateError):
                gate.submit(self.root, self.task, "plan", files)

    def test_state_symlink_cannot_read_or_write_outside_project(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / ".codex/local").mkdir(parents=True)
            (self.root / ".codex/local/gates").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(gate.GateError):
                gate.load(self.root, self.task)
            with self.assertRaises(gate.GateError):
                self.submit("issue")
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_two_approvals_allow_implementation_and_pr_open(self):
        self.approved_plan()
        for stage in ("implement", "pr-open"):
            self.assertTrue(gate.check(self.root, self.task, stage)["allowed"])

    def test_each_approved_document_change_blocks_implementation(self):
        self.approved_plan()
        for name in ("issue.md", "spec.md", "plan.md", "tasks.md"):
            path = self.root / name
            before = path.read_bytes()
            path.write_text("changed revision")
            with self.subTest(name=name), self.assertRaises(gate.GateError):
                gate.check(self.root, self.task, "implement")
            path.write_bytes(before)

    def test_resubmission_revokes_downstream_approval(self):
        self.approved_plan()
        self.submit("issue")
        self.human("issue")
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "implement")

    def test_piped_approval_is_rejected_without_mutation(self):
        self.submit("issue")
        before = gate.state_path(self.root, self.task).read_bytes()
        with self.assertRaises(gate.GateError):
            gate.decide(self.root, self.task, "issue", "approved", "test", io.StringIO(), io.StringIO())
        self.assertEqual(gate.state_path(self.root, self.task).read_bytes(), before)

    def test_wrong_confirmation_does_not_approve(self):
        self.submit("issue")
        incoming, outgoing = io.StringIO("yes\n"), io.StringIO()
        incoming.isatty = outgoing.isatty = lambda: True
        with self.assertRaises(gate.GateError):
            gate.decide(self.root, self.task, "issue", "approved", "test", incoming, outgoing)
        self.assertEqual(gate.load(self.root, self.task)["gates"]["issue"]["decision"], "pending")

    def test_missing_empty_and_external_documents_are_rejected(self):
        (self.root / "empty.md").touch()
        for name in ("missing.md", "empty.md", "../outside.md"):
            with self.subTest(name=name), self.assertRaises(gate.GateError):
                gate.submit(self.root, self.task, "issue", [name])

    def test_invalid_task_and_corrupt_state_fail_closed(self):
        with self.assertRaises(gate.GateError):
            gate.load(self.root, "../escape")
        self.submit("issue")
        gate.state_path(self.root, self.task).write_text("[]")
        with self.assertRaises(gate.GateError):
            gate.load(self.root, self.task)

    def test_pr_requires_committed_clean_checkout_and_real_url(self):
        self.approved_plan()
        with self.assertRaises(gate.GateError):
            self.submit("pr")
        self.real_git()
        with self.assertRaises(gate.GateError):
            gate.submit(self.root, self.task, "pr", ["pr.md"], "not-a-pr")
        (self.root / "unreviewed.py").write_text("# new code")
        with self.assertRaises(gate.GateError):
            self.submit("pr")

    def test_pr_review_fix_resubmit_and_human_merge_handoff(self):
        self.approved_plan()
        self.real_git()
        self.submit("pr")
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "review-fix")
        self.human("pr", "changes_requested")
        self.assertTrue(gate.check(self.root, self.task, "review-fix")["allowed"])
        self.submit("pr")
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "handoff-merge")
        self.human("pr")
        self.assertTrue(gate.check(self.root, self.task, "handoff-merge")["allowed"])
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "merge")

    def test_new_commit_invalidates_pr_approval(self):
        self.approved_plan()
        run = self.real_git()
        self.submit("pr")
        self.human("pr")
        (self.root / "code.py").write_text("# changed code")
        run("add", "code.py")
        run("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-qm", "new revision")
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "handoff-merge")

    def test_merge_is_denied_even_without_task_state(self):
        with self.assertRaises(gate.GateError):
            gate.check(self.root, self.task, "merge")

    def test_submission_changed_during_review_is_not_approved(self):
        self.submit("issue")
        entry = gate.load(self.root, self.task)["gates"]["issue"]
        incoming, outgoing = io.StringIO(), io.StringIO()
        incoming.isatty = outgoing.isatty = lambda: True
        def changed():
            (self.root / "issue.md").write_text("new version while reviewing")
            return f"approved {self.task} issue {entry['digest']}\n"
        incoming.readline = changed
        with self.assertRaises(gate.GateError):
            gate.decide(self.root, self.task, "issue", "approved", "test", incoming, outgoing)


if __name__ == "__main__":
    unittest.main()
