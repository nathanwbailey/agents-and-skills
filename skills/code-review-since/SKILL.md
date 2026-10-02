---
name: code-review-since
description: Review and commit the currently staged Git changes. Use when the user asks to review staged changes and commit them with a good message; the review and commit are always limited to the Git index.
---

# Staged review and commit

Invocation authorizes one local commit containing exactly the staged snapshot that is reviewed.

## 1. Pin the staged snapshot

Use `git diff --cached --quiet` to require a non-empty index. Stop with a concise explanation when nothing is staged.

Record the staged tree with:

```bash
git write-tree
```

Treat that tree hash as the exact review unit.

Read the change only from Git objects, never from worktree-only content:

- Use `git diff --name-status HEAD <tree> --`, `git diff --check HEAD <tree> --`, and `git diff HEAD <tree> --` for the review surface.
- Use `git show <tree>:<path>` for the reviewed version of a changed file.
- Use `git show HEAD:<path>` for tracked baseline context.
- When additional repository context is needed, prefer committed `HEAD` content rather than ordinary worktree reads.
- Keep unstaged and untracked content outside the review.
- Leave the index and worktree unchanged.

## 2. Delegate the review

If you are the coordinating/main agent, delegate the review to the `reviewer` subagent (Agent tool, `subagent_type: reviewer`).

Give the reviewer:

- the recorded tree hash;
- the instruction to review the diff from `HEAD` to that exact tree;
- any applicable repository instructions already identified.

The reviewer is read-only. It must not edit files, stage files, commit, amend, or otherwise mutate the repository.

If you are already executing as the `reviewer` subagent, perform the review yourself. Do not spawn another reviewer for the same task.

Review every staged hunk for concrete:

- correctness defects;
- behavior regressions;
- unsafe behavior or security issues;
- broken contracts or invalid assumptions;
- error-handling problems;
- missing or inadequate tests.

Apply relevant repository instructions and documented conventions. Prioritize actionable defects over style-only comments.

Return findings ordered by severity. Identify each finding with the reviewed staged file and line when possible, explain the impact, and give a specific correction. If there are no findings, say so explicitly.

The coordinating agent must surface the review result to the user before committing. Feedback is advisory: do not silently fix, stage, or alter the reviewed snapshot.

## 3. Verify and commit the same snapshot

Run `git write-tree` again immediately before committing.

- If the tree still equals the reviewed tree, continue.
- If it changed, restart the review once using the new tree.
- If it changes a second time, stop and ask the user to stabilize the index.

Derive a concise imperative commit message from the reviewed diff's primary intent, then run:

```bash
git commit -m "<message>"
```

Do not add files, amend another commit, bypass hooks, or intentionally include worktree-only content.

If a hook or Git rejects the commit, report the failure and stop.

After the commit, confirm that the commit tree equals the reviewed tree. If it does not, report the mismatch explicitly and stop; do not amend or create another commit automatically.

Report:

- the review findings, including an explicit no-findings result;
- the commit hash and message;
- confirmation that the resulting commit tree matches the reviewed staged tree.
