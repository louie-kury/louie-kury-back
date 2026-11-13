"""The project-local reset must work without installing a plugin or its hooks."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[2] / ".agents/skills/vibe-wise-reset/reset.py"


class VibeWiseResetTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="학습 메모 검사 ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        (self.root / ".git").mkdir()

    def run_helper(self, *args):
        result = subprocess.run([sys.executable, "-B", str(HELPER), "--cwd", str(self.root), *args],
                                capture_output=True, text=True, timeout=5)
        return result.returncode, json.loads(result.stdout)

    def notes(self):
        state = self.root / ".vibe-wise"
        state.mkdir()
        for name in ("profile.md", "progress.md", "project-map.md"):
            (state / name).write_text("# Existing fixture " + name)
        return state

    def test_missing_notes_does_not_create_state(self):
        code, result = self.run_helper()
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "no_notes")
        self.assertFalse((self.root / ".vibe-wise").exists())

    def test_preview_does_not_change_notes_and_changed_notes_invalidate_confirmation(self):
        state = self.notes()
        before = {p.name: p.read_bytes() for p in state.iterdir()}
        code, preview = self.run_helper()
        self.assertEqual(code, 0)
        self.assertEqual(preview["status"], "preview")
        self.assertEqual({p.name: p.read_bytes() for p in state.iterdir()}, before)
        (state / "progress.md").write_text("new decision while reviewing")
        after = {p.name: p.read_bytes() for p in state.iterdir()}
        code, result = self.run_helper("--confirm", preview["confirmation"])
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "error")
        self.assertEqual({p.name: p.read_bytes() for p in state.iterdir()}, after)

    def test_confirmed_fixture_reset_preserves_original_notes_in_backup(self):
        state = self.notes()
        before = {p.name: p.read_bytes() for p in state.iterdir()}
        _, preview = self.run_helper()
        code, result = self.run_helper("--confirm", preview["confirmation"])
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "reset")
        backup = Path(result["backup"])
        for name, data in before.items():
            self.assertEqual((backup / name).read_bytes(), data)
        self.assertIn("Onboarding: incomplete", (state / "profile.md").read_text())


if __name__ == "__main__":
    unittest.main()
