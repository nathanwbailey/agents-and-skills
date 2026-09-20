---
name: explore
description: Explore a codebase read-only and return an evidence-backed map. Use when the user explicitly asks to explore or trace code, or when another skill needs verified structure, ownership, or flow evidence.
---

# Explore

Investigate from a concrete anchor and stop at the narrowest boundary that answers the question. The caller's requested output contract takes precedence over this skill's default.

The child agent may search and read files but must leave the workspace unchanged. Ask it to return evidence, inferences, and unresolved questions rather than edits or recommendations outside the requested scope.

## Process

1. **Parent — scope:** State the question, concrete anchor, and depth. Use medium depth unless the caller requests another level.
2. **Parent — delegate:** Render `agents/explorer.prompt.tmpl` with `{QUESTION}` = the bounded investigation question, `{ANCHOR}` = the concrete anchor, `{DEPTH}` = requested depth (default `medium`), `{ANGLE}` = "overall", and `{OUTPUT_EXTRA}` = the child handoff format below. Spawn the `explorer` agent (`subagent_type: explorer`, defined in `agents/explorer.md`) with that rendered prompt before exploring locally. The agent has a read-only tool surface and returns the child handoff below. If delegation is unavailable, report that the exploration cannot follow this skill and stop.
3. **Child — investigate:** The `explorer` agent locates the anchor and applicable repository instructions, resolves ambiguous or duplicate anchors, then follows definitions, callers, callees, tests, and configuration only where they affect the question. It checks competing implementations when ownership is unclear.
4. **Child — report:** Return the child handoff defined below.
5. **Parent — verify and integrate:** Incorporate the child's evidence, perform any necessary local follow-up, and ensure every material claim meets the same evidence standard.
6. **Parent — stop:** Finish when the original question is answered, the controlling owner, path, or boundary is evidenced, and every remaining unknown explains why the available evidence was insufficient.

## Depth

- **Quick:** identify the anchor, owning definition, and direct relationships.
- **Medium:** establish the controlling path, meaningful branches, and tests or configuration that constrain it.
- **Thorough:** examine alternate implementations, subsystem boundaries, failure paths, and unresolved searches.

Escalate depth only when the current level cannot answer the question.

## Output

### Child handoff to parent

The child returns:

1. **Findings** — observed behavior with a precise `path:line` reference for every material claim.
2. **Inferences** — conclusions not directly established by the cited code, labeled as inference.
3. **Search gaps** — unresolved questions, what was searched, and why the evidence was insufficient.
4. **Files read** — every file the child read.

### Parent response to caller

The parent integrates and verifies the child handoff, then returns the caller's requested format. When the caller provides no format, return:

1. **Direct answer** — the smallest useful conclusion.
2. **Evidence map** — key `path:line` references and the role of each location.
3. **Flow or relationships** — only the sequence, ownership, or dependencies needed to answer the question.
4. **Uncertainty or search gaps** — distinguish missing evidence from inference.
5. **Next inspection target** — include only when something material remains unresolved.
