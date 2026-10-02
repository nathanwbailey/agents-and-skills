---
name: review-session
description: Review only the files changed in the current task by pinning a temporary Git snapshot and delegating independent standards and spec reviews.
disable-model-invocation: true
---

# Review session

Review only files this task changed. Exclude files already dirty at task start unless this task also changed them; mark such files as mixed.

1. Build the snapshot with `python ${CLAUDE_SKILL_DIR}/scripts/session_tree.py <repo-relative-path>...`. It uses a temporary Git index and prints a tree hash.
2. Confirm `git diff --name-status HEAD <tree>` is exactly the review scope.
3. Collect the user request or linked specification, applicable `CLAUDE.md`/`AGENTS.md` and standards documents, and `SMELLS.md`.
4. Spawn two `reviewer` subagents in parallel with the Agent tool (`subagent_type: reviewer`): one for standards and one for the specification. Give both the tree hash, scope, mixed files, and artifact paths. Wait for both before continuing.
5. Report separate `## Standards` and `## Spec` results with finding count and worst issue. Do not merge their conclusions into one verdict.

If no files changed, report `no session changes`.
