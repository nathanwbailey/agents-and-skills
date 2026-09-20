import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills/review-session/scripts/session-tree.sh"


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


class SessionTree(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp())
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        for name in ("a.txt", "c.txt", "gone.txt"):
            (self.repo / name).write_text("base\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")
        (self.repo / "a.txt").write_text("session edit\n")
        (self.repo / "b.txt").write_text("session new\n")
        (self.repo / "c.txt").write_text("someone else's edit\n")
        (self.repo / "gone.txt").unlink()

    def run_script(self, *paths):
        return subprocess.run([str(SCRIPT), *paths], cwd=self.repo, capture_output=True, text=True)

    def test_tree_holds_only_the_named_paths(self):
        out = self.run_script("a.txt", "b.txt", "gone.txt")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(
            git(self.repo, "diff", "--name-status", "HEAD", out.stdout.strip(), "--"),
            "M\ta.txt\nA\tb.txt\nD\tgone.txt\n",
        )

    def test_unnamed_dirty_file_keeps_its_head_content(self):
        tree = self.run_script("a.txt").stdout.strip()
        self.assertEqual(git(self.repo, "show", f"{tree}:c.txt"), "base\n")

    def test_index_and_worktree_are_untouched(self):
        before = git(self.repo, "status", "--porcelain")
        self.run_script("a.txt", "b.txt")
        self.assertEqual(git(self.repo, "status", "--porcelain"), before)
        self.assertEqual((self.repo / "a.txt").read_text(), "session edit\n")

    def test_works_from_a_subdirectory(self):
        (self.repo / "sub").mkdir()
        out = subprocess.run([str(SCRIPT), "a.txt"], cwd=self.repo / "sub", capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(git(self.repo, "diff", "--name-status", "HEAD", out.stdout.strip(), "--"), "M\ta.txt\n")

    def test_unknown_path_fails_with_its_name(self):
        out = self.run_script("nope.txt")
        self.assertEqual((out.returncode, out.stderr), (1, "unknown path: nope.txt\n"))

    def test_no_paths_prints_usage(self):
        out = self.run_script()
        self.assertEqual(out.returncode, 2)
        self.assertIn("usage:", out.stderr)


if __name__ == "__main__":
    unittest.main()
