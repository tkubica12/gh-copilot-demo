---
name: agenticWorkflow
description: Draft a GitHub Agentic Workflow that augments CI/CD with guarded automation.
agent: planner
---
Design a GitHub Agentic Workflow (`gh-aw`) for this repository.

Requirements:

- keep deterministic CI/CD intact
- describe the markdown workflow source and the compiled `.lock.yml` concept
- use read-only permissions by default
- use safe outputs for any GitHub write action
- explain where the workflow fits relative to coding agents, code review, and security

Return:

1. workflow purpose
2. recommended trigger
3. recommended permissions
4. safe outputs
5. a draft markdown workflow body
