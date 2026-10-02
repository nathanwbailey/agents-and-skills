---
name: explore
description: Explore a codebase and return an evidence-backed map. Reuse summaries for source files outside documentation. Use when asked to trace code or gather context for a repository file.
---

# Explore

Investigate from a concrete anchor and stop at the narrowest boundary that answers the question. Read Markdown and documentation files directly. For another named repository file, check its mirrored summary before searching its contents. The caller's requested response format takes precedence over the default below.

## File summary workflow

Do not create summaries for Markdown (`.md`, `.mdx`, `.markdown`), other documentation files (`.rst`, `.adoc`), or any file under `doc/`, `docs/`, or `documentation/`. Read these sources directly.

For another named file, use `python <this-skill>/scripts/summary_cache.py check --repo <repository-root> --source <repo-relative-path>`. The command prints `fresh`, `missing`, `stale`, `missing-source`, or `skipped`, followed by the summary path. A fresh summary is a starting point, not proof that it answers every question. Read the source when the question needs details the summary lacks or when current behavior matters. Treat a stale summary as context only until source investigation refreshes it.

After exploring an eligible file in a writable session, the coordinating agent writes a concise Markdown body, then calls `python <this-skill>/scripts/summary_cache.py write --repo <repository-root> --source <repo-relative-path> --body-file <draft-path>`. The helper adds the source path and SHA-256 hash and writes `summaries/<repo-relative-path>.md`, preserving the source suffix. It rejects documentation. Do not write a summary for a missing source. Do not create summaries during read-only or planning work; report the findings in chat instead. A fresh, sufficient summary needs no rewrite.

Every summary creation or edit must include a hash freshly computed from the current source with CRLF normalized to LF. Use the helper for all writes, including wording-only summary edits; it updates the source path and hash atomically. The checker also accepts older hashes written from CRLF checkouts, while new writes use the normalized form. When the source has not changed, its correct hash remains the same. Never copy an old hash into a revised summary or update a hash without checking that the summary body still describes the source.

The body covers the file's purpose and behavior, key definitions and dependencies, relevant `path:line` evidence, and unresolved questions. Include the callable surface, inputs, outputs, and side effects when those details matter to the question. A summary is concise reusable context, not a replacement for current source evidence.

## Investigation

1. State the question, anchor, and depth. Use medium depth unless the caller requests quick or thorough investigation.
2. Delegate a bounded, read-only question to the `explorer` agent (Agent tool, `subagent_type: explorer`). It follows definitions, callers, tests, and configuration only where they affect the answer. If delegation is unavailable, investigate directly.
3. Verify the returned evidence. Label inferences and search gaps, and cite a precise `path:line` for every material claim.
4. For an eligible non-documentation file, create or refresh its summary when investigation changed what is known and writing is allowed.
5. Answer when the controlling path or owner is evidenced and remaining unknowns have been stated.

The explorer agent remains read-only. The coordinating agent owns summary writes.

## Depth and response

- **Quick:** anchor, owning definition, and direct relationships.
- **Medium:** controlling path, meaningful branches, and constraining tests or configuration.
- **Thorough:** alternate implementations, subsystem boundaries, failure paths, and unresolved searches.

Return a direct answer, the smallest useful evidence map, relevant flow, and uncertainty. Include a next inspection target only when something material remains unresolved.
