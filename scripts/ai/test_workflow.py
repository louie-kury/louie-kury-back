"""Read-only Spec Kit analysis must not change the active feature pointer."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ReadOnlyAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="읽기 전용 workflow ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        scripts = self.root / ".specify/scripts/bash"
        shutil.copytree(ROOT / ".specify/scripts/bash", scripts)
        self.feature = self.root / "specs/001-analysis"
        self.feature.mkdir(parents=True)
        for name in ("spec.md", "plan.md", "tasks.md"):
            (self.feature / name).write_text("# Isolated analysis fixture\n")
        self.pointer = self.root / ".specify/feature.json"

    def analyze_prerequisites(self):
        env = dict(os.environ, SPECIFY_INIT_DIR=str(self.root),
                   SPECIFY_FEATURE_DIRECTORY=str(self.feature), SPECIFY_FEATURE_NO_PERSIST="1")
        result = subprocess.run([
            "bash", str(self.root / ".specify/scripts/bash/check-prerequisites.sh"),
            "--json", "--require-spec", "--require-tasks", "--include-tasks"
        ], env=env, cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(json.loads(result.stdout)["FEATURE_DIR"]), self.feature)

    def test_analysis_does_not_create_pointer(self):
        self.analyze_prerequisites()
        self.assertFalse(self.pointer.exists())

    def test_analysis_preserves_other_features_existing_pointer_bytes(self):
        self.pointer.write_text('{"feature_directory":"specs/999-other"}\n')
        before = self.pointer.read_bytes()
        self.analyze_prerequisites()
        self.assertEqual(self.pointer.read_bytes(), before)
