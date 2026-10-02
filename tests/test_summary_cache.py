from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "explore" / "scripts" / "summary_cache.py"
SPEC = importlib.util.spec_from_file_location("summary_cache", SCRIPT)
assert SPEC and SPEC.loader
summary_cache = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(summary_cache)


class SummaryCache(unittest.TestCase):
    def test_create_reuse_and_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve()
            source = repo / "src" / "model.py"
            source.parent.mkdir()
            source.write_text("VALUE = 1\n", encoding="utf-8")
            self.assertEqual(summary_cache.status(repo, "src/model.py")[0], "missing")
            summary = summary_cache.write_summary(repo, "src/model.py", "# Model\n\nVALUE is one.")
            self.assertEqual(summary, repo / "summaries" / "src" / "model.py.md")
            self.assertIn("# Model", summary.read_text(encoding="utf-8"))
            self.assertEqual(summary_cache.status(repo, "src/model.py")[0], "fresh")
            source.write_text("VALUE = 2\n", encoding="utf-8")
            self.assertEqual(summary_cache.status(repo, "src/model.py")[0], "stale")
            summary_cache.write_summary(repo, "src/model.py", "# Model\n\nVALUE is two.")
            self.assertEqual(summary_cache.status(repo, "src/model.py")[0], "fresh")
            summary.write_text(summary.read_text(encoding="utf-8").replace("src/model.py", "wrong.py"), encoding="utf-8")
            self.assertEqual(summary_cache.status(repo, "src/model.py")[0], "stale")

    def test_missing_source_and_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary).resolve()
            self.assertEqual(summary_cache.status(repo, "missing.py")[0], "missing-source")
            with self.assertRaises(FileNotFoundError):
                summary_cache.write_summary(repo, "missing.py", "No source")
            with self.assertRaises(ValueError):
                summary_cache.status(repo, "../outside.py")
            with self.assertRaises(ValueError):
                summary_cache.status(repo, str(repo / "missing.py"))


if __name__ == "__main__":
    unittest.main()
