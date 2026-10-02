from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "review-session" / "scripts" / "session_tree.py"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, text=True, capture_output=True).stdout


class SessionTree(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(self.repo, ignore_errors=True))
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.test")
        git(self.repo, "config", "user.name", "t")
        for name in ("a.txt", "c.txt", "gone.txt"):
            (self.repo / name).write_text("base\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")
        (self.repo / "a.txt").write_text("session edit\n", encoding="utf-8")
        (self.repo / "b.txt").write_text("session new\n", encoding="utf-8")
        (self.repo / "c.txt").write_text("someone else's edit\n", encoding="utf-8")
        (self.repo / "gone.txt").unlink()

    def run_script(self, *paths: str, cwd: Path | None = None):
        return subprocess.run([sys.executable, str(SCRIPT), *paths], cwd=cwd or self.repo, text=True, capture_output=True)

    def test_tree_holds_only_named_paths(self) -> None:
        out = self.run_script("a.txt", "b.txt", "gone.txt")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(git(self.repo, "diff", "--name-status", "HEAD", out.stdout.strip(), "--"), "M\ta.txt\nA\tb.txt\nD\tgone.txt\n")

    def test_index_and_worktree_are_untouched(self) -> None:
        before = git(self.repo, "status", "--porcelain")
        self.run_script("a.txt", "b.txt")
        self.assertEqual(git(self.repo, "status", "--porcelain"), before)
        self.assertEqual((self.repo / "a.txt").read_text(encoding="utf-8"), "session edit\n")

    def test_unknown_path_and_usage_fail(self) -> None:
        unknown = self.run_script("nope.txt")
        self.assertEqual((unknown.returncode, unknown.stderr), (1, "unknown path: nope.txt\n"))
        usage = self.run_script()
        self.assertEqual(usage.returncode, 2)
        self.assertIn("usage:", usage.stderr)


if __name__ == "__main__":
    unittest.main()
