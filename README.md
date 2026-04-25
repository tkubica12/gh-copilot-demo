# GitHub Copilot Demo

This repository is a guided workshop for demonstrating GitHub Copilot across repository context, skills, MCP, custom agents, Copilot CLI, governance, workflow automation, and operations.

The detailed lecture has moved from one giant README into chapter files under [`docs\workshop`](docs\workshop\README.md). This root README is now the landing page and navigation hub.

## Workshop chapters

| Chapter | Topic |
| --- | --- |
| [00](docs\workshop\00-course-map.md) | Course map and whole story |
| [01](docs\workshop\01-repository-context.md) | Repository context, AGENTS.md, PRD, specs, and Spaces |
| [02](docs\workshop\02-skills-and-mcp.md) | Skills and MCP |
| [03](docs\workshop\03-vscode-agents.md) | VS Code prompt files, custom agents, handoffs, and subagents |
| [04](docs\workshop\04-copilot-cli.md) | Copilot CLI execution, sessions, research, memory, and execution surfaces |
| [05](docs\workshop\05-token-efficiency.md) | Token efficiency, context hygiene, and measurement lab results |
| [06](docs\workshop\06-governance-review-security-hooks.md) | Governance, review, security, hooks, and Critic agent |
| [07](docs\workshop\07-workflow-agents.md) | Workflow agents in GitHub Actions |
| [08](docs\workshop\08-operations.md) | SRE agents and operations |
| [09](docs\workshop\09-optional-demos.md) | Optional demos and extensions |

## Token-efficiency benchmark highlight

The course now includes a measured token-efficiency lab. The headline lecture table is in [Chapter 05](docs\workshop\05-token-efficiency.md), with detailed results in [`tools\copilot-token-lab\suite-example-analysis.md`](tools\copilot-token-lab\suite-example-analysis.md) and rerun instructions in [`tools\copilot-token-lab\README.md`](tools\copilot-token-lab\README.md).

## Supporting material

- [`AGENTS.md`](AGENTS.md) defines repository-wide Copilot instructions.
- [`PRD.md`](PRD.md) and [`specs\`](specs\) provide product and architecture context.
- [`docs\enterprise_demo_flow.md`](docs\enterprise_demo_flow.md) is the concise presenter flow.
- [`.github\prompts`](.github\prompts) and [`.github\skills`](.github\skills) contain reusable Copilot starts and local capabilities.
- [`tools\copilot-token-lab`](tools\copilot-token-lab\README.md) contains the token measurement side project.

This repository is for demonstrations and learning, not for production use.
