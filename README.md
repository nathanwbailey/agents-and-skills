# agents-and-skills

Personal collection of Claude Code skills and subagents.

- `skills/` — one directory per skill, each with a `SKILL.md`
- `agents/` — Claude Code subagent definitions. Every agent pins `model: claude-sonnet-5` and `effort: medium`
- `tests/` — `python3 -m unittest discover tests` checks that every agent a skill spawns exists in `agents/`, that every agent pins the model and effort, that no file names another editor, a remote agent, or a non-Claude model, and that `install.sh` installs into `~/.claude`
- `install.sh` — copies `skills/` to `~/.claude/skills` and `agents/` to `~/.claude/agents`

## Install

```sh
./install.sh
```

Flags:

- `--force` — overwrite anything already installed (default: skip existing items)
- `--dry-run` — print what would happen without writing anything
- `--list` — list the skills and agents in this repo and exit

Skills must not pass `model` when they spawn a repo agent. A spawn-time `model` overrides the agent's pin.
