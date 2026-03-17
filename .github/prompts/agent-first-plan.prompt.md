---
mode: agent
description: Plan a repository change with the right mix of AGENTS.md, custom agents, skills, validation, and handoffs.
---
Use the repository root `AGENTS.md` plus any relevant `.github` assets to plan the requested work before editing.

Return:

- the objective,
- likely files or folders,
- the best agent breakdown,
- whether `/fleet` is useful if the client supports parallel task execution,
- where a skill helps,
- whether MCP is required for live data or remote systems,
- validation steps,
- the first implementation step.

Do not edit files unless the user explicitly asks for implementation.
