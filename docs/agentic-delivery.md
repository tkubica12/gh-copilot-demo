# Agentic delivery

This chapter is the main bridge from simple Copilot assistance to practical engineering execution.

## Why it matters

- Copilot can take ownership of a bounded task instead of only suggesting snippets.
- Editor-first and terminal-first delivery styles each have a place.
- Custom agents and subagent patterns matter because specialization improves quality and speed.

## What to explore

1. VS Code agent mode with a concrete implementation task.
2. Copilot CLI for shell-native work such as planning, testing, repo inspection, or automation.
3. Custom agents that specialize roles.
4. Subagents or `/fleet`-style delegation when the work naturally splits into parallel tracks.

## Core narrative

Modern Copilot is most convincing when it can:

- inspect the repository
- propose a plan
- edit multiple files
- run tests or commands
- recover from mistakes
- produce something reviewable

## Surfaces to cover

### VS Code agent mode

This surface works especially well for:

- the tight local edit-run-fix loop
- interactive steering while the code evolves in front of the team
- showing that the agent can reason over files, tests, and architecture together

### Copilot CLI

This surface works especially well for:

- terminal-native engineering work
- model selection and automation flags
- specialized agents for exploration, tasks, planning, and review
- explicit context inspection and resumable workflows

The CLI reinforces that agentic delivery is not tied to a single editor surface.

Helpful CLI details to highlight:

- `/model` for model choice during the session
- built-in specialist agents such as Explore, Task, Plan, and Code-review
- `/context`, `/compact`, and `/tasks` for session visibility and control
- `copilot -p`, `--silent`, and sharing options for automation and handoff

## Custom agents in this repository

The repository already includes focused custom agents under `.github\agents\`:

- `workshop-orchestrator.agent.md`
- `plan-and-handoff.agent.md`
- `workshop-implementer.agent.md`
- `workshop-reviewer.agent.md`

These examples make role specialization concrete:

- orchestration
- planning and handoff
- focused implementation
- validation and review

## Subagents and fleet-style delegation

When a task has independent tracks, a lead agent can delegate work instead of stuffing everything into one prompt.

Good examples:

- parallel specialists for repo investigation
- one agent preparing a handoff for another
- `/fleet` or similar parallel delegation when the client supports it

The core pattern is simple: one orchestrator, several bounded specialists, one merged outcome.

## Repository examples

- [`.github/agents/README.md`](../.github/agents/README.md)
- [`.github/prompts/fleet-breakdown.prompt.md`](../.github/prompts/fleet-breakdown.prompt.md)
- `examples\agents\01-cli-orchestration-and-handoff.md`
- `examples\agents\03-long-running-agent-pattern.md`
- [`enterprise_demo_flow.md`](enterprise_demo_flow.md)

## Supporting material

- `examples\agents\README.md`
- [`README.md`](../README.md)
