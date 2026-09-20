#!/usr/bin/env bash
# Prints the hash of a git tree equal to HEAD plus the current content of the
# given repo-relative paths (created, edited, or deleted). The real index and
# worktree are never touched.
set -euo pipefail

[ $# -gt 0 ] || { echo "usage: session-tree.sh <repo-relative-path>..." >&2; exit 2; }

cd "$(git rev-parse --show-toplevel)"

for p in "$@"; do
  if [ ! -e "$p" ] && ! git cat-file -e "HEAD:$p" 2>/dev/null; then
    echo "unknown path: $p" >&2
    exit 1
  fi
done

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
export GIT_INDEX_FILE="$scratch/index"

git read-tree HEAD
git add -A -- "$@"
git write-tree
