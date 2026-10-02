---
name: create-engineering-verification-skill
description: Create a repository-local Claude Code skill that verifies an engineering workflow through its public entry point and observable results. Use for agent runtimes, tool services, data pipelines, and other systems where different claims need different proof layers.
---

# Create an engineering verification skill

Create a reusable verification skill in the target repository, following its skill location and naming conventions. A fresh Claude Code session should be able to run it without private chat context. This creator is suited to repositories that combine configuration-driven applications, tool or service boundaries, stateful artifacts, and optional external systems; it does not assume a particular SDK, language, framework, or deployment platform.

## Establish the claim

Inspect repository instructions, relevant specs or design documents, the production entry point, configuration, existing harnesses, and the code behind the behavior. Treat documents as design guidance and reconcile them with current source and observed behavior when they differ. Identify what a caller can observe, which dependencies the workflow owns, and which are external.

State the verification claim, acceptance criteria, constraints, and exclusions before choosing a drive. Keep distinct entry points and configurations distinct: for example, a local profile, a deployed profile, and a separately assembled graph may have different tool access and guarantees. Follow the target repository's approval rules before changing tests, specs, production code, or external state.

## Match proof to the claim

Choose the narrowest production-facing path that can establish the claim. Existing tests may be the primary proof when they call the public boundary and assert caller-visible behavior; a live run is needed only for a claim about live dependencies or end-to-end operation.

| Claim | Appropriate evidence |
| --- | --- |
| Tool or service behavior | Invoke the registered tool, API route, command, or message handler the client uses. Assert its output and failure behavior. Replace only dependencies outside that boundary. |
| Application assembly and routing | Load the real configuration through its builder or runner. With controlled external adapters where appropriate, inspect available tools, routes, state updates, and final results. |
| Stateful artifact hand-off | Follow returned IDs or handles through the next public operation. Read the stored object when authorized and verify the relevant values or bytes; metadata alone may be insufficient. |
| Real model or external service behavior | Use an opt-in, bounded run through the production-facing entry point. Capture requests, tool calls, intermediate state, returned artifacts, and the final result. |
| Deployment wiring | Exercise a safe preflight, health route, discovery call, or deployed request appropriate to the claim. Separate configuration checks from proof that a live deployment works. |

Label each check by the layer it actually exercised: hermetic contract, in-process integration, live model or service, or deployed system. A graph build does not prove a remote service is available; a mock-backed tool check does not prove real credentials or data access. Conversely, do not require an expensive live run to establish deterministic matching, routing, or calculation behavior.

## Write the generated skill

Give its `SKILL.md` a discriminating name and description. Include the target repository's actual entry point, exact commands, inputs, prerequisites, expected observations, evidence location, and the limits of each check. Derive interpreter, package manager, environment, and test commands from that repository rather than copying this creator's examples.

Reuse an existing harness when it reaches the claimed boundary. Add a helper under `scripts/` only if repeatable driving or evidence inspection needs one; do not require fixed subcommands or a new harness for every workflow. Add a workflow map only when several capabilities need separate instructions. If useful, adapt the [optional map example](references/workflow-map-example/README.md). A separate endpoint skill is warranted only when endpoint verification is a substantial independent workflow.

Evidence should show the configuration or tool used, inputs, observed outputs, exit status, and any intermediate state or artifact needed to substantiate the claim. Protect secrets and sensitive data. If a prerequisite is missing, record the exact blocker and the claim left unproven. Do not present an offline or partial check as a successful live proof.

## Verify and hand off

Check prerequisites without changing shared state. Use an isolated run ID, namespace, or scratch location for writes. Run the chosen proof, inspect its result, and clean up only resources that run created while preserving reviewable evidence. Before retrying a failed job that may consume compute or mutate external state, determine what the first attempt did.

Validate the generated skill's frontmatter and links with an available skill validator, and run any new helper against a representative safe path. Follow the target repository's test, lint, and approval policies for any accompanying code changes. Report what passed, what was skipped, and what each result actually proves.
