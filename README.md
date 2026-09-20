# agents-and-skills

Personal collection of Claude/Codex/Cursor-style skills and subagents, kept in one place and installable across tools with a single script.

- `skills/` — one directory per skill, each with a `SKILL.md` (same format across Claude Code, Codex, and Cursor)
- `agents/` — Markdown subagent definitions (Claude Code format)
- `install.sh` — installs everything into whichever local tool config directories exist on this machine

## Install

```sh
./install.sh --all
```

Or target specific tools:

```sh
./install.sh --claude          # ~/.agents/skills (+ symlinks in ~/.claude/skills), ~/.claude/agents
./install.sh --codex           # ~/.codex/skills
./install.sh --cursor          # ~/.cursor/skills-cursor
./install.sh --vscode          # no-op: the Claude Code VSCode extension shares ~/.claude
```

With no flags, it installs into every tool whose config directory already exists.

Other flags:

- `--force` — overwrite anything already installed at the destination (default: skip existing items, leave them untouched)
- `--dry-run` — print what would happen without writing anything
- `--list` — list the skills and agents in this repo and exit

## Notes

- Codex subagents are defined per-project as TOML (`.codex/agents/*.toml`), a different format from the Markdown agents here, so `agents/` is not auto-converted for Codex — port manually if needed.
- No global Cursor subagent directory was found on this machine, so `agents/` is not installed for Cursor either.
- Skill format (`SKILL.md` with YAML frontmatter: `name`, `description`, optional `disable-model-invocation`, etc.) is shared across Claude Code, Codex, and Cursor, so skills install unmodified into all three.
