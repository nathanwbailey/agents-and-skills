# agents-and-skills

Claude Code skills and subagents for reusable local workflows.

- `skills/` holds 25 skills selected for AI/ML product engineering and supporting software workflows. Twelve are explicit-only (`disable-model-invocation: true`); invoke them as `/skill-name`, for example `/handoff`.
- `agents/` holds three subagents: `explorer` (read-only exploration), `reviewer` (read-only review of a pinned Git snapshot), and `general-purpose` (scoped worker).
- `install.py` copies both into `~/.claude/skills` and `~/.claude/agents`.

`explore` checks `summaries/<repo-relative-source-path>.md` before searching a named source file, and the coordinating agent refreshes that summary after investigating. A source hash marks stale summaries.

## Install

```sh
python3 install.py
```

- `--list` lists source items without copying.
- `--dry-run` shows the planned copies.
- `--force` replaces existing items; otherwise they are skipped.

## Validate

```sh
python3 -m unittest discover -s tests -v
python3 tests/validate_repo.py
```
