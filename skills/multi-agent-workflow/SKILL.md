---
name: multi-agent-workflow
description: Coordinates user-defined sub-agents across a Copilot workflow. Use when the user asks for multi-agent coordination, staged implementation, parallel exploration, handoffs, or a review pass.
---

# Multi-Agent Workflow

## Quick Start

Use this skill when the task should be split across multiple agents and the user wants to define what each sub-agent does.

1.⁠ ⁠Ask the user to name at least two sub-agents and describe each one’s responsibility.
2.⁠ ⁠Spawn every requested sub-agent before doing any implementation work.
3.⁠ ⁠Keep every sub-agent narrowly scoped to one concrete output.
4.⁠ ⁠Merge the results into a single coordinated plan or change.

## Workflow

•⁠  ⁠Require the user to define the sub-agents and what each one should do.
•⁠  ⁠Ensure at least two agents are spawned whenever this skill is used.
•⁠  ⁠Prefer parallel execution when sub-agents can work independently.
•⁠  ⁠Pass only the evidence the next agent needs.
•⁠  ⁠Stop widening scope once the controlling path is identified.

## Prompt Template

⁠ text
Use a multi-agent pass on this task.

Sub-agent 1: [name] - [responsibility]
Sub-agent 2: [name] - [responsibility]
Sub-agent 3: [name] - [responsibility]

Do not proceed until the sub-agent list is explicitly defined.
Spawn the requested sub-agents and combine their outputs.
 ⁠

## Guardrails

•⁠  ⁠Use one concrete output per agent.
•⁠  ⁠Keep changes small and reversible.
•⁠  ⁠If the task is ambiguous, ask the user to define the sub-agents before spawning them.
•⁠  ⁠If a spawned agent finds a mismatch, send the task back to the smallest relevant agent instead of broadening the search.