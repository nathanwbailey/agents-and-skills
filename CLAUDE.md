# Claude Code library

Personal collection of Claude Code skills and subagents.

- Skills live in `skills/<name>/SKILL.md` with `name` and `description` frontmatter. Skills that should only run when invoked explicitly set `disable-model-invocation: true`.
- Subagents live in `agents/<name>.md` with `name`, `description`, `tools`, and `model` frontmatter. Skills spawn them with the Agent tool and `subagent_type`.
- Keep portable helpers in Python and write text files as UTF-8.

Validate changes with:

```sh
python3 -m unittest discover -s tests -v
python3 tests/validate_repo.py
```
