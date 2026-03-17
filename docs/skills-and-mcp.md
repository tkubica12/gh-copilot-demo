# Skills and MCP

This chapter shows how to make agents more useful by giving them repeatable local capabilities and access to live systems.

## Why it matters

- Skills and MCP solve different problems and work better together than apart.
- Repository-local skills complement custom agents by making good patterns reusable.
- MCP connects agents to current external data and systems.

## Simple decision rule

- use a **skill** when the capability should live with the repository
- use **MCP** when the capability depends on a live remote system or tool

## Skills in this repository

[`.github/skills/README.md`](../.github/skills/README.md) provides the entry point, followed by these concrete examples:

- `agent-first-workshop-patterns`
- `json-to-xml-converter`
- `simplecontext`

Skills are a good fit for:

- reusable domain context
- repeatable local guidance
- lightweight script-backed actions

## MCP in this repository

MCP shows how Copilot reaches beyond the repository:

- `mcp\random_string_mcp\` as a simple local server example
- GitHub MCP for issues, pull requests, workflow runs, and code search
- Azure MCP for cloud resources and troubleshooting
- Kubernetes MCP for operations and diagnosis
- database and Playwright style integrations when the story needs live systems

## What to explore

1. One small skill-based task.
2. One MCP-backed task using live or current information.
3. How skills and MCP combine inside a larger agent workflow.

## Repository examples

- [`.github/skills/README.md`](../.github/skills/README.md)
- `examples\agents\02-mcp-and-approval-aware-workflow.md`
- `mcp\random_string_mcp\`

## What to emphasize

- skills improve repeatability without requiring a remote integration
- MCP makes agents practical on real systems because it adds deterministic tools and current data
- custom agents, skills, and MCP each solve a different layer of the problem

## Supporting material

- [`.github/skills/README.md`](../.github/skills/README.md)
- `examples\agents\02-mcp-and-approval-aware-workflow.md`
- [`README.md`](../README.md)
