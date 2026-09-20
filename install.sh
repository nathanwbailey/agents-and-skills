#!/usr/bin/env bash
# Installs the skills/ and agents/ in this repo into local AI tool config dirs.
#
# Usage:
#   ./install.sh [--claude] [--codex] [--cursor] [--vscode] [--all]
#                [--force] [--dry-run] [--list]
#
# With no target flags, installs into every tool whose config directory
# already exists on this machine. --force overwrites items that already
# exist at the destination (default: skip existing, leave them alone).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENTS_SRC="$SCRIPT_DIR/agents"

FORCE=0
DRY_RUN=0
LIST=0
WANT_CLAUDE=0
WANT_CODEX=0
WANT_CURSOR=0
WANT_VSCODE=0
ANY_TARGET_FLAG=0

for arg in "$@"; do
  case "$arg" in
    --claude) WANT_CLAUDE=1; ANY_TARGET_FLAG=1 ;;
    --codex) WANT_CODEX=1; ANY_TARGET_FLAG=1 ;;
    --cursor) WANT_CURSOR=1; ANY_TARGET_FLAG=1 ;;
    --vscode) WANT_VSCODE=1; ANY_TARGET_FLAG=1 ;;
    --all) WANT_CLAUDE=1; WANT_CODEX=1; WANT_CURSOR=1; WANT_VSCODE=1; ANY_TARGET_FLAG=1 ;;
    --force) FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --list) LIST=1 ;;
    -h|--help)
      sed -n '2,10p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 1
      ;;
  esac
done

if [ "$LIST" -eq 1 ]; then
  echo "Skills ($(ls "$SKILLS_SRC" | wc -l | tr -d ' ')):"
  ls "$SKILLS_SRC"
  echo
  echo "Agents ($(ls "$AGENTS_SRC" | wc -l | tr -d ' ')):"
  ls "$AGENTS_SRC"
  exit 0
fi

# Claude Code (and the VSCode extension, which shares the same config)
# reads skills from ~/.claude/skills and agents from ~/.claude/agents.
# ~/.agents/skills is a convention some setups use for the real skill
# files, with ~/.claude/skills symlinking into it; if that layout is
# already in place here, keep using it, otherwise copy directly.
copy_or_link_skill() {
  local name="$1" dest_dir="$2" src="$SKILLS_SRC/$1"
  local dest="$dest_dir/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$FORCE" -eq 1 ]; then
      [ "$DRY_RUN" -eq 1 ] || rm -rf "$dest"
    else
      echo "  skip (exists): $name"
      return 0
    fi
  fi
  echo "  install: $name -> $dest_dir"
  [ "$DRY_RUN" -eq 1 ] && return 0
  cp -R "$src" "$dest"
}

copy_agent() {
  local name="$1" dest_dir="$2" src="$AGENTS_SRC/$1"
  local dest="$dest_dir/$name"
  if [ -e "$dest" ]; then
    if [ "$FORCE" -eq 1 ]; then
      [ "$DRY_RUN" -eq 1 ] || rm -f "$dest"
    else
      echo "  skip (exists): $name"
      return 0
    fi
  fi
  echo "  install: $name -> $dest_dir"
  [ "$DRY_RUN" -eq 1 ] && return 0
  cp "$src" "$dest"
}

symlink_skill() {
  local name="$1" claude_skills_dir="$2" real_dir="$3"
  local link="$claude_skills_dir/$name"
  if [ -e "$link" ] || [ -L "$link" ]; then
    if [ "$FORCE" -eq 1 ]; then
      [ "$DRY_RUN" -eq 1 ] || rm -rf "$link"
    else
      return 0
    fi
  fi
  [ "$DRY_RUN" -eq 1 ] && return 0
  ln -s "$real_dir/$name" "$link"
}

install_claude() {
  local agents_skills="$HOME/.agents/skills"
  local claude_skills="$HOME/.claude/skills"
  local claude_agents="$HOME/.claude/agents"

  echo "== Claude Code =="
  mkdir -p "$agents_skills" "$claude_skills" "$claude_agents"
  for s in $(ls "$SKILLS_SRC"); do
    copy_or_link_skill "$s" "$agents_skills"
    symlink_skill "$s" "$claude_skills" "$agents_skills"
  done
  for a in $(ls "$AGENTS_SRC"); do
    copy_agent "$a" "$claude_agents"
  done
}

install_vscode() {
  # The Claude Code VSCode extension reads the same ~/.claude config as
  # the CLI, so there is nothing extra to install here.
  echo "== VSCode (Claude Code extension) =="
  echo "  shares ~/.claude config with Claude Code; nothing extra to do"
}

install_codex() {
  local dest="$HOME/.codex/skills"
  echo "== Codex CLI =="
  if [ ! -d "$HOME/.codex" ]; then
    echo "  ~/.codex not found, skipping (pass --codex to force)"
    return
  fi
  mkdir -p "$dest"
  for s in $(ls "$SKILLS_SRC"); do
    copy_or_link_skill "$s" "$dest"
  done
  echo "  note: Codex agent subagents use per-project TOML files (.codex/agents/*.toml)."
  echo "  the Markdown agents in agents/ are not auto-converted; port manually if needed."
}

install_cursor() {
  local dest="$HOME/.cursor/skills-cursor"
  echo "== Cursor =="
  if [ ! -d "$HOME/.cursor" ]; then
    echo "  ~/.cursor not found, skipping (pass --cursor to force)"
    return
  fi
  mkdir -p "$dest"
  for s in $(ls "$SKILLS_SRC"); do
    copy_or_link_skill "$s" "$dest"
  done
  echo "  note: no global Cursor subagent directory found; agents/ not installed here."
}

if [ "$ANY_TARGET_FLAG" -eq 0 ]; then
  [ -d "$HOME/.claude" ] && WANT_CLAUDE=1
  [ -d "$HOME/.codex" ] && WANT_CODEX=1
  [ -d "$HOME/.cursor" ] && WANT_CURSOR=1
  [ -d "$HOME/.claude" ] && WANT_VSCODE=1
fi

[ "$WANT_CLAUDE" -eq 1 ] && install_claude
[ "$WANT_CODEX" -eq 1 ] && install_codex
[ "$WANT_CURSOR" -eq 1 ] && install_cursor
[ "$WANT_VSCODE" -eq 1 ] && install_vscode

echo
if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run complete, nothing was written."
else
  echo "Done."
fi
