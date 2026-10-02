# Optional workflow verification map

Use a map when one verification skill covers capabilities with different entry points, dependencies, or proof layers. Each page should name a caller-visible claim and the evidence that would establish it. A single-capability skill can keep this information in `SKILL.md`.

## Example capabilities

- [Application assembly](application-build.md): configuration, available tools, and routing.
- [Live agent turn](live-agent-turn.md): an opt-in request through a model and tool services.

A tool-service skill might instead map discovery, object loading, transformation, and artifact retrieval. Follow returned IDs or handles between operations and inspect stored objects where the claim depends on their contents.

For each capability, record the target repository's actual command or call, inputs, prerequisites, expected observations, evidence location, and proof layer. A skipped live check leaves its live claim unproven while narrower passing checks retain their own value.
