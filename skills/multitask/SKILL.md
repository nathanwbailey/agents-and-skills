---
name: multitask
description: Multitask across asynchronous subagents. Use when the user asks to multitask, parallelize pending work, or split a large request into independent chunks that can run concurrently.
---

# Multitask

Turn the user's requests into a dependency-aware task board and keep every safe concurrency slot doing useful work. The root agent owns coordination, integration, and the final answer.

## 1. Build the work graph

Break the request and any pending additive messages into the smallest independently completable tasks. Record dependencies and distinguish ready tasks from blocked tasks. Keep tightly coupled work together when splitting would create coordination overhead or conflicting edits.

This step is complete when every requested outcome has one owner and every task can state its concrete deliverable.

## 2. Assign safe ownership

Parallelize read-only work freely. For editing work, give agents disjoint files or directories; reserve shared integration files for the root agent. Agents share one workspace, so their edits become visible immediately and require no branch merge. Record the initial working-tree state before spawning editors so pre-existing changes remain attributable.

Give each subagent:

- one bounded objective;
- the minimum context and inputs it needs;
- its owned files, or an explicit read-only constraint;
- a checkable deliverable and validation requirement;
- relevant authorization and repository constraints.

Each editor preserves pre-existing changes in its owned files and reports them separately. Its writes, staging, reverts, formatting, and other mutations stay inside its ownership. Worker validation is limited to owned paths and read-only checks; the root agent runs repository-wide mutating formatters and full validation after integration.

Use `list_agents` to account for occupied slots. Fill the available slots with ready tasks without waiting between spawns. The root agent should take an independent task when that helps throughput; otherwise it coordinates and integrates.

This step is complete when every running agent has non-overlapping ownership and a checkable completion criterion.

## 3. Run the asynchronous queue

Use `spawn_agent` for the first wave. While agents run, progress root-owned work and send concise user updates. Treat new additive user messages as queue entries. Before scheduling one, update the dependency graph and ownership map; work touching a path owned by a running agent remains blocked until that owner finishes or is explicitly redirected. When a new message replaces earlier work, interrupt or redirect only the affected agents.

As each agent finishes:

1. Inspect its result and shared-workspace changes.
2. Send a focused follow-up when its deliverable is incomplete.
3. Start the next ready task in the freed slot.
4. Route discovered work to the smallest relevant owner instead of widening every agent's scope.

Wait only when no root-owned or newly ready work remains. This step is complete when the queue is empty and every agent deliverable has been accepted or explicitly reported as blocked.

## 4. Integrate and verify

Review the combined result as one change. Resolve cross-task inconsistencies centrally, then run the repository-required checks against the integrated state. Send a failed check back to the smallest responsible task when parallel correction remains safe; otherwise fix it serially at the integration point.

Keep Git history operations with the root agent unless the user explicitly assigns them elsewhere. Preserve the user's authorization boundaries throughout the fleet.

Finish with one coherent report covering completed tasks, material decisions, validation evidence, and any unresolved risk. The multitask run is complete only when every requested outcome and required check is accounted for.

## Boundaries

This skill emulates asynchronous decomposition and scheduling. It does not provide Cursor's worktree isolation, Agents Window UI, or multi-root workspace feature. When safe edit ownership cannot be partitioned, parallelize investigation and review, then perform implementation serially.
