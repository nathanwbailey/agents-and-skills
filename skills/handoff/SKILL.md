---
name: handoff
description: Create a redacted, portable handoff document for continuing work in a later Claude Code session. Use when pausing, transferring ownership, or preserving a resume point.
disable-model-invocation: true
---

# Handoff

Write a portable Markdown handoff. Ask for an output path when the user supplied one; otherwise write `.claude/handoffs/<UTC timestamp>-<slug>.md`. Never auto-commit it.

Redact secrets, credentials, personal data, and private tool output. Reference existing plans, decisions, diffs, commits, issues, and verification output instead of copying them.

Use these sections:

1. Goal and current status.
2. Worktree and branch, including whether it is dirty.
3. Decisions made and their evidence.
4. Files changed and verification completed.
5. Open risks, blockers, and the next smallest action.
6. Suggested skills and named subagents.

Confirm the final path. A later session uses this document as input; it must not require private session logs.
