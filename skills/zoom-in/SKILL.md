---
name: zoom-in
description: Answer specific questions about code features, implementation details, and architecture decisions by delegating read-only investigation to the `explorer` agent. Use when the user asks "How does X work?", "Where is Y implemented?", "Why was X designed this way?", or needs details about a specific feature or function.
---

# Zoom In

Answer specific architecture and implementation questions about code by using the `explorer` agent to gather focused context, then synthesize a direct answer.

## Quick start

When a user asks a specific question about code:

1. **Start from the concrete anchor** — identify the file, symbol, feature, or module the question targets
2. **Invoke `explorer`** — spawn it with `subagent_type: explorer`, the anchor, and the narrowest useful depth
3. **Request focused findings** — ask for key files, call flow, design rationale, and any uncertainty relevant to the question
4. **Answer directly** — synthesize the subagent findings into a concise explanation tied to the user's question

## Workflows

### "How does feature X work?"

- Ask `explorer` to trace the main entry point and 2-3 levels of the relevant call flow
- Request the major data transformations or branching decisions
- Summarize the purpose of each layer for the user
- Extract the core pattern in 1-2 sentences

### "Where is Y implemented?"

- Ask `explorer` to find the symbol, its owning module, and the most relevant call sites
- Request nearby helpers or utilities that complete the implementation
- Explain why that location appears to own the behavior
- Link the answer to the most relevant files returned by the subagent

### "Why was X designed this way?"

- Ask `explorer` to find the code implementing the decision and any local signals of intent
- Request related patterns elsewhere in the codebase if they sharpen the rationale
- Offer the likely constraints that shaped the design
- Tie the explanation back to the project's domain language or stated goals when possible

## Advanced features

Use the domain vocabulary from your project's CONTEXT.md or ADRs when explaining design. Link back to architectural decisions when they apply. If the answer requires naming conventions or patterns specific to the project, ground your explanation in those terms. Keep the subagent prompt narrow and concrete so the returned context stays useful for a direct answer.