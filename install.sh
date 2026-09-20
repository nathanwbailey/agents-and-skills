#!/usr/bin/env bash
# Installs skills/ into ~/.claude/skills and agents/ into ~/.claude/agents.
#
# Usage: ./install.sh [--force] [--dry-run] [--list]
#
# Existing items are skipped unless --force is passed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENTS_SRC="$SCRIPT_DIR/agents"
SKILLS_DEST="$HOME/.claude/skills"
AGENTS_DEST="$HOME/.claude/agents"

FORCE=0
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --list)
      echo "Skills:"; ls "$SKILLS_SRC"
      echo; echo "Agents:"; ls "$AGENTS_SRC"
      exit 0
      ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

install_item() {
  local src="$1" dest_dir="$2"
  local name dest
  name="$(basename "$src")"
  dest="$dest_dir/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$FORCE" -eq 0 ]; then
      echo "  skip (exists): $name"
      return 0
    fi
    [ "$DRY_RUN" -eq 1 ] || rm -rf "$dest"
  fi
  echo "  install: $name -> $dest_dir"
  [ "$DRY_RUN" -eq 1 ] || cp -R "$src" "$dest"
}

[ "$DRY_RUN" -eq 1 ] || mkdir -p "$SKILLS_DEST" "$AGENTS_DEST"

echo "== Skills =="
for s in "$SKILLS_SRC"/*/; do install_item "${s%/}" "$SKILLS_DEST"; done
echo "== Agents =="
for a in "$AGENTS_SRC"/*; do install_item "$a" "$AGENTS_DEST"; done

echo
if [ "$DRY_RUN" -eq 1 ]; then echo "Dry run complete, nothing was written."; else echo "Done."; fi
