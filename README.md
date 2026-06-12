# GitHub Copilot Demo

This repository is a guided workshop for demonstrating GitHub Copilot across repository context, skills, MCP, custom agents, Copilot CLI, governance, workflow automation, and operations.

The detailed lecture has moved from one giant README into chapter files under [`docs/workshop`](docs/workshop/README.md). This root README is now the landing page and navigation hub.

Language: [EN](README.md) | [CZ workshop](docs/workshop/README_CZ.md) | [CZ enterprise flow](docs/enterprise_demo_flow_CZ.md)

> Canonical source of truth: English (`EN`) files are canonical. Czech (`CZ`) files are mirrors for local delivery.

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

## Workshop chapters (CZ mirrors)

| Kapitola | Téma |
| --- | --- |
| [01](docs/workshop/01-repository-context_CZ.md) | Kontext repozitáře, AGENTS.md, PRD, specifikace a Spaces |
| [02](docs/workshop/02-skills-and-mcp_CZ.md) | Skills a MCP |
| [03](docs/workshop/03-vscode-agents_CZ.md) | VS Code prompt soubory, custom agenti, handoffy a subagenti |
| [04](docs/workshop/04-copilot-cli_CZ.md) | Copilot CLI execution, sessions, research, memory a execution surfaces |
| [05](docs/workshop/05-token-efficiency_CZ.md) | Tokenová efektivita, context hygiene a výsledky měřicí laboratoře |
| [06](docs/workshop/06-governance-review-security-hooks_CZ.md) | Governance, review, security, hooks a Critic agent |
| [07](docs/workshop/07-workflow-agents_CZ.md) | Workflow agenti v GitHub Actions |
| [08](docs/workshop/08-operations_CZ.md) | SRE agenti a operations |
| [09](docs/workshop/09-optional-demos_CZ.md) | Volitelné demoukázky a rozšíření |

## Token-efficiency benchmark highlight

The course now includes a measured token-efficiency lab. The headline lecture table is in [Chapter 05](docs/workshop/05-token-efficiency.md), with detailed results in [`tools/copilot-token-lab/suite-example-analysis.md`](tools/copilot-token-lab/suite-example-analysis.md) and rerun instructions in [`tools/copilot-token-lab/README.md`](tools/copilot-token-lab/README.md). Use the companion article [Token saving in GitHub Copilot](https://tomaskubica.cz/en/2026/token-saving-cz/) for the longer narrative and keep the repo chapter focused on measured workshop evidence.

## Supporting material

- [`AGENTS.md`](AGENTS.md) defines repository-wide Copilot instructions.
- [`PRD.md`](PRD.md) and [`specs/`](specs/) provide product and architecture context.
- [`docs/enterprise_demo_flow.md`](docs/enterprise_demo_flow.md) is the concise presenter flow.
- [`docs/enterprise_demo_flow_CZ.md`](docs/enterprise_demo_flow_CZ.md) is the Czech mirror of the presenter flow.
- [`.github/prompts`](.github/prompts) and [`.github/skills`](.github/skills) contain reusable Copilot starts and local capabilities.
- [`tools/copilot-token-lab`](tools/copilot-token-lab/README.md) contains the token measurement side project.
- [Agent skills and central management](https://tomaskubica.cz/en/2026/agent-skills-centralni-sprava/) complements the local skills chapter with central operating-model guidance.

This repository is for demonstrations and learning, not for production use.
