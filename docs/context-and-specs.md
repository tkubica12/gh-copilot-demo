# Context and specs

This chapter explains why agents become reliable only when they operate inside clear repository guidance, explicit specs, and reusable context.

## Why it matters

- `AGENTS.md` is a visible part of the delivery system, not background metadata.
- Specs and prompt assets reduce ambiguity before implementation starts.
- Repository context connects naturally to Copilot Memory and Copilot Spaces.

## What to explore

1. `AGENTS.md` and the repository rules it defines.
2. `specs\` as the source of project and service contracts.
3. Prompt files and reusable task framing.
4. Local context discipline together with Copilot Memory and Spaces.

## Context layers in this repository

### `AGENTS.md`

[`AGENTS.md`](../AGENTS.md) acts as the house rules for:

- coding conventions
- documentation expectations
- testing discipline
- implementation logging

This is a clear way to demonstrate that agents should not invent their own operating model on every task.

### Specs and spec-kit style workflows

`specs\` shows that reliable agentic delivery depends on explicit contracts, not only on clever prompting.

One useful framing is the spec-kit style flow:

`clarify -> plan -> tasks -> implement`

That sequence shows how exploration becomes repeatable execution.

### Prompt and handoff assets

This repo also uses prompt-shaped assets and handoff patterns so context can survive across agents and sessions.

## Memory and shared context

Position the broader context story like this:

- repository instructions provide the most controllable guidance
- Copilot Memory reduces re-explanation across recurring work
- Copilot Spaces package reusable shared context for a team or scenario

## What to emphasize

- strong outcomes come from layered context, not from longer prompts alone
- `AGENTS.md`, specs, and reusable prompts are inspectable by humans
- shared context should improve handoff, planning, and review across tools

## Supporting material

- [`AGENTS.md`](../AGENTS.md)
- `specs\`
- [`README.md`](../README.md)
