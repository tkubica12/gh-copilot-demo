<!-- omit from toc -->
# GitHub Copilot Workshop Repository

This repository is organized as a customer-facing workshop for modern GitHub Copilot. It follows a practical story from quick wins, to agentic delivery, to context and guidance, to skills and MCP, to Agent HQ and multi-agent orchestration, and finally to governed delivery with code review, security review, workflow agents, and Azure SRE Agent.

> [!IMPORTANT]
> This repository is optimized for workshops, customer conversations, and hands-on exploration. It favors clear patterns, realistic examples, and broad platform coverage over production hardening.

## Workshop flow

The summary table below maps the main journey through the repository. The numbered chapters that follow add a short description of each stop in that journey.

| Chapter | Focus | Why it matters | Deep dive |
| --- | --- | --- | --- |
| 1 | Basics | Establishes quick wins, model choice, search, edits, and Spark as the on-ramp | [`docs/basics.md`](docs/basics.md) |
| 2 | Agentic delivery | Shows practical delivery across VS Code, Copilot CLI, custom agents, subagents, and `/fleet` | [`docs/agentic-delivery.md`](docs/agentic-delivery.md) |
| 3 | Context and specs | Explains how `AGENTS.md`, specs, and spec-kit style flows make agents reliable | [`docs/context-and-specs.md`](docs/context-and-specs.md) |
| 4 | Skills and MCP | Clarifies how local reusable capabilities and live external tools work together | [`docs/skills-and-mcp.md`](docs/skills-and-mcp.md) |
| 5 | Agent HQ and orchestration | Covers multi-agent orchestration, background agents, and cloud agents | [`docs/agent-hq-and-orchestration.md`](docs/agent-hq-and-orchestration.md) |
| 6 | Governed delivery | Connects code review, security review, workflow agents, and Azure SRE Agent into one operating model | [`docs/governed-delivery.md`](docs/governed-delivery.md) |

### 1. Basics

This chapter introduces the quick wins that make GitHub Copilot approachable: model choice, chat, search, targeted edits, and a short Spark moment for natural-language app creation. It matters because it establishes the platform entry points without letting the story stall in a basic feature tour.
**Deep dive:** [`docs/basics.md`](docs/basics.md)

### 2. Agentic delivery

This chapter moves into the heart of the workshop: agents that can plan, edit, test, recover, and produce something reviewable. It matters because it shows the shift from isolated assistance to practical delivery across VS Code, Copilot CLI, custom agents, subagents, and `/fleet`-style delegation.
**Deep dive:** [`docs/agentic-delivery.md`](docs/agentic-delivery.md)

### 3. Context and specs

This chapter explains why good outcomes do not come from prompting alone. It matters because `AGENTS.md`, repository conventions, specs, and spec-kit style flows turn capable models into reliable delivery systems.
**Deep dive:** [`docs/context-and-specs.md`](docs/context-and-specs.md)

### 4. Skills and MCP

This chapter explains how agents become useful on real work by combining reusable local capabilities with live external tools. It matters because it gives customers a clean mental model for when to use skills, when to use MCP, and how the two work together.
**Deep dive:** [`docs/skills-and-mcp.md`](docs/skills-and-mcp.md)

### 5. Agent HQ and orchestration

This chapter shows how work moves from one useful agent to coordinated multi-agent execution across local, background, and cloud surfaces. It matters because it introduces Agent HQ, orchestration choices, long-running tasks, and the management layer needed for modern agent operations.
**Deep dive:** [`docs/agent-hq-and-orchestration.md`](docs/agent-hq-and-orchestration.md)

### 6. Governed delivery

This chapter closes with the controls that make agentic engineering enterprise-ready: code review, security review, workflow agents, approvals, auditability, and Azure SRE Agent. It matters because it shows how agents fit inside an operating model with visible governance rather than bypassing it.
**Deep dive:** [`docs/governed-delivery.md`](docs/governed-delivery.md)

## What this repository emphasizes

- **Agents as practical collaborators** for coding, testing, review, research, and automation
- **Custom agents and subagents** for specialization, delegation, and bounded parallel work
- **Copilot CLI** as a first-class execution surface for terminal-native agent workflows
- **`AGENTS.md`, specs, and spec-driven development** as the reliability layer for agent outcomes
- **Skills and MCP** as complementary capability layers: local reusable capabilities plus live external tools
- **Agent HQ / mission control** for orchestration across local, background, and cloud execution
- **Governed delivery** through pull requests, checks, security controls, auditability, and workflow agents

### Workshop agenda

- [`docs/copilot_workshop_agenda_EN.md`](docs/copilot_workshop_agenda_EN.md)
- [`docs/copilot_workshop_agenda_CZ.md`](docs/copilot_workshop_agenda_CZ.md)

## Repository map

| Path | Purpose |
| --- | --- |
| [`docs/`](docs) | Main workshop chapters, agenda files, and supporting material |
| [`AGENTS.md`](AGENTS.md) | Repository-wide operating instructions for agents |
| [`specs/`](specs) | Platform and service specifications for spec-driven delivery |
| [`.github/agents/`](.github/agents) | Custom agent examples for orchestration, implementation, handoff, and review |
| [`.github/skills/`](.github/skills) | Skills guidance and concrete skill examples |
| [`.github/prompts/`](.github/prompts) | Prompt assets for planning, delegation, handoff, and skill/MCP choices |
| [`.github/chatmodes/`](.github/chatmodes) | Chat mode assets for guided exploration sessions |
| [`examples/`](examples) | Self-contained scenarios including new agent orchestration examples |
| [`mcp/`](mcp) | MCP server examples and related tooling |
| [`src/`](src) | Application and service code used in implementation, testing, and review demos |
| [`.github/workflows/`](.github/workflows) | Existing CI/CD plus illustrative workflow-agent patterns |

