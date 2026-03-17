---
name: agent-first-workshop-patterns
description: Guide planning, subagent handoffs, optional /fleet parallelization, and review loops for this workshop repository.
---

# Agent-first workshop patterns

Use this skill when the task is about teaching, designing, or demonstrating how several Copilot customization layers work together in this repo.

## What this skill is for

- choosing between direct execution, a custom agent, a skill, and MCP,
- packaging handoffs between planner, implementer, and reviewer roles,
- spotting work that can be parallelized with `/fleet` when the client supports it,
- keeping workshop examples grounded in the repository root `AGENTS.md`.

## Recommended workflow

1. Start from the user outcome, not the tool.
2. Reuse `AGENTS.md` for standing rules.
3. Split the work into planning, implementation, validation, and review.
4. Use `/fleet` only when the tracks are truly independent and the client supports that feature.
5. Prefer skills for reusable local patterns and MCP for live remote systems.

## Handoff template

- objective,
- files in scope,
- assumptions,
- validation step,
- next owner,
- final response format.

## Example prompts

- "Show how you would break this feature into planner, implementer, and reviewer agents."
- "Is this a skill, an MCP integration, or both?"
- "What parts of this repo update are worth parallelizing with `/fleet`, if it is available?"
