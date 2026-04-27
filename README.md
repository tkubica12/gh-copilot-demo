# GitHub Copilot Demo

This repository is a guided workshop for demonstrating GitHub Copilot across repository context, skills, MCP, custom agents, Copilot CLI, governance, workflow automation, and operations.

The detailed lecture has moved from one giant README into chapter files under [`docs/workshop`](docs/workshop/README.md). This root README is now the landing page and navigation hub.

## Whole story at a glance

The workshop follows one connected engineering story:

- [**Shape Copilot behavior with repository context**](docs/workshop/01-repository-context.md) — how Copilot is guided by repository instructions, product intent, specifications, and shared planning context.
- [**Skills and MCP**](docs/workshop/02-skills-and-mcp.md) — how Copilot gains capabilities through packaged local skills and connected tools.
- [**Plan and specialize work in VS Code**](docs/workshop/03-vscode-agents.md) — prompt files, custom agents, handoffs, and subagents working together.
- [**Continue execution in Copilot CLI**](docs/workshop/04-copilot-cli.md) — plan mode, execution, review, research, session history, and execution surfaces.
- [**Save tokens with context hygiene**](docs/workshop/05-token-efficiency.md) — scoped context, progressive reveal, compression, and OpenTelemetry-backed measurement.
- [**Govern delivery with review, security, and hooks**](docs/workshop/06-governance-review-security-hooks.md) — code generation is not the end; add cross-model review with the Critic agent.
- [**Add workflow agents in GitHub Actions**](docs/workshop/07-workflow-agents.md) — repository automation after merge.
- [**Operate with SRE agents**](docs/workshop/08-operations.md) — closing the loop with operational thinking and OpenTelemetry observability.

## Workshop chapters

| Chapter | Topic |
| --- | --- |
| [01](docs/workshop/01-repository-context.md) | Repository context, AGENTS.md, PRD, specs, and Spaces |
| [02](docs/workshop/02-skills-and-mcp.md) | Skills and MCP |
| [03](docs/workshop/03-vscode-agents.md) | VS Code prompt files, custom agents, handoffs, and subagents |
| [04](docs/workshop/04-copilot-cli.md) | Copilot CLI execution, sessions, research, memory, and execution surfaces |
| [05](docs/workshop/05-token-efficiency.md) | Token efficiency, context hygiene, and measurement lab results |
| [06](docs/workshop/06-governance-review-security-hooks.md) | Governance, review, security, hooks, and Critic agent |
| [07](docs/workshop/07-workflow-agents.md) | Workflow agents in GitHub Actions |
| [08](docs/workshop/08-operations.md) | SRE agents and operations |
| [09](docs/workshop/09-optional-demos.md) | Optional demos and extensions |

## Token-efficiency benchmark highlight

The course now includes a measured token-efficiency lab. The headline lecture table is in [Chapter 05](docs/workshop/05-token-efficiency.md), with detailed results in [`tools/copilot-token-lab/suite-example-analysis.md`](tools/copilot-token-lab/suite-example-analysis.md) and rerun instructions in [`tools/copilot-token-lab/README.md`](tools/copilot-token-lab/README.md).

## Supporting material

- [`AGENTS.md`](AGENTS.md) defines repository-wide Copilot instructions.
- [`PRD.md`](PRD.md) and [`specs/`](specs/) provide product and architecture context.
- [`docs/enterprise_demo_flow.md`](docs/enterprise_demo_flow.md) is the concise presenter flow.
- [`.github/prompts`](.github/prompts) and [`.github/skills`](.github/skills) contain reusable Copilot starts and local capabilities.
- [`tools/copilot-token-lab`](tools/copilot-token-lab/README.md) contains the token measurement side project.

This repository is for demonstrations and learning, not for production use.
