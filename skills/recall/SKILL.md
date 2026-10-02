---
name: recall
description: Reconstruct working context from an explicit handoff, decision log, Git or PR state, current-chat context, and user-provided evidence. Use for catch-up or resuming work without private-session access.
disable-model-invocation: true
---

# Recall

Build a tight current-state brief without reading private chat storage or assuming session-file locations.

1. Prefer a user-supplied handoff or decision log. Then inspect the current chat, Git history and status, linked PRs/issues, and explicitly supplied evidence.
2. State any missing source instead of filling gaps from memory.
3. Verify claims against live repository or PR state when that evidence is available.
4. Return a capsule of no more than five bullets, thread status, open problems, and the single best next action.

Separate observations from inferences. A request to recover a different chat that has no portable artifact requires the user to provide its handoff or evidence.
