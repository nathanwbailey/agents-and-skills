---
name: review-session
description: Review only the changes this session made, using the reviewer agent on a pinned snapshot, along Standards and Spec axes.
disable-model-invocation: true
---

# Review Session

Review the **session diff**: the files this conversation created, edited, or deleted, and nothing else in the worktree. Two `reviewer` agents run in parallel, one per axis, so neither pollutes the other's context.

- **Standards** — does the change follow this repo's documented standards and avoid the smell baseline?
- **Spec** — does the change do what the request asked, and do it correctly?

## Process

### 1. List the session files

Walk your own Edit, Write, and Bash calls in this conversation and list every repo-relative path you created, edited, or deleted. Leave out any file you only read, and any file that was already dirty at session start (see the start-of-session `git status`) unless you also changed it.

Done when every path in the list traces to a tool call of yours. An empty list ends the skill: report "no session changes".

### 2. Pin the snapshot

Run `scripts/session-tree.sh <path>...` from this skill's directory. It prints a tree hash equal to `HEAD` plus those paths, built in a temporary index.

Done when `git diff --name-status HEAD <tree>` lists exactly your session files. An extra or missing path means fix the list and pin again.

A file that was dirty at session start and that you also edited carries the user's changes too. Name it as **mixed** in both briefs so the reviewers weigh it accordingly.

### 3. Find the sources

- **Spec:** the user's request in this conversation, then any issue or spec file it points at. With no spec anywhere, skip the Spec reviewer and say so in the report.
- **Standards:** repo documents such as `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or a coding-standards file, plus [SMELLS.md](SMELLS.md).

Two rules bind the smells. A documented repo standard beats the baseline. Every smell is a labelled judgement call ("possible Feature Envy"), never a hard violation, and anything tooling already enforces is skipped.

### 4. Spawn both reviewers

One message, two `Agent` calls, `subagent_type: reviewer`. Each brief carries the tree hash, the mixed-file list, and its axis.

**Standards brief.** The standards files, plus the full text of [SMELLS.md](SMELLS.md) pasted in, since the reviewer has no other access to it. Ask for every place the change breaks a documented standard (cite file and rule) and every baseline smell (name it, quote the hunk). Hard violations and judgement calls stay separate. Under 400 words.

**Spec brief.** The spec text. Ask for requirements missing or partial, behaviour nobody asked for, and requirements that look implemented but look wrong. Quote the spec line for each. Under 400 words.

Done when both reports are back.

### 5. Report

Present `## Standards` and `## Spec` verbatim or lightly cleaned. The axes stay separate because a change can pass one and fail the other. End with one line per axis: finding count and worst issue. Pick no winner across axes.
