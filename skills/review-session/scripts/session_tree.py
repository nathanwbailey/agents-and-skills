#!/usr/bin/env python3
"""Print a tree for HEAD plus the current content of named repo paths.

The real index and worktree are never changed.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def git(*args: str, cwd: Path, env: dict[str, str] | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True, text=True, capture_output=True).stdout


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: session_tree.py <repo-relative-path>...", file=sys.stderr)
        return 2
    try:
        root = Path(git("rev-parse", "--show-toplevel", cwd=Path.cwd()).strip())
    except subprocess.CalledProcessError:
        print("not in a git repository", file=sys.stderr)
        return 1
    for raw_path in argv:
        path = root / raw_path
        exists_in_head = subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{raw_path}"], cwd=root, capture_output=True
        ).returncode == 0
        if not path.exists() and not exists_in_head:
            print(f"unknown path: {raw_path}", file=sys.stderr)
            return 1
    with tempfile.TemporaryDirectory(prefix="claude-session-tree-") as temporary:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        git("read-tree", "HEAD", cwd=root, env=env)
        git("add", "-A", "--", *argv, cwd=root, env=env)
        print(git("write-tree", cwd=root, env=env).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
