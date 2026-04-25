[Workshop index](README.md) | [Repository README](..\..\README.md)

---

# 2. Shape Copilot behavior with repository context

This chapter explains how Copilot is guided **before** it starts making changes.

## 2.1 Concepts to explain first

This chapter is about durable context, not specialization yet.

| Concept | Best use |
| --- | --- |
| **AGENTS.md** | Always-on repository rules and engineering preferences |
| **PRD and specs** | Product intent, architecture, contracts, testing, security, and service boundaries |
| **Constitution and spec-kit** | A repeatable way to bootstrap and evolve spec-driven delivery |
| **Copilot Spaces** | Shared planning context across repositories, documents, and teams |

The easiest way to explain the relationship is:

- `AGENTS.md` teaches Copilot how this repository works
- `PRD.md` and `specs\` explain what the system is supposed to do
- constitutions and templates keep specifications consistent across projects
- Copilot Spaces help when the planning context is larger than one repository

Prompt files, custom agents, handoffs, and hooks are still important, but they are easier to teach once the audience has seen how the repository itself provides context.

## 2.2 AGENTS.md in depth

Open `AGENTS.md` and walk through it. This is the most important single file for shaping Copilot behavior.

VS Code with GitHub Copilot fully supports the [AGENTS.md](https://agents.md/) standard. You can also place `AGENTS.md` in subfolders for monorepo situations where different services have different rules.

**Note**: Apart from repository custom instructions, you can also configure [personal custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions) for your own preferences and [organization custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions) for team-wide standards.

### Tips on what to include in AGENTS.md

- **Coding style** — Terraform structure, code structure, use Pydantic, etc.
- **Frameworks and tools** — use FastAPI, uv as package manager, use azurerm provider in Terraform, use Helm charts rather than Kustomize, etc.
- **Procedures and recommendations** — always check solution design, keep implementation log, common errors
- **Tests and ad-hoc artifacts** — prefer regular testing, when using something ad-hoc prefix it and delete afterwards
- **Common environments and configuration styles** — use `.env`, check envs directly vs. use config class, etc.
- **Documentation strategy** — use docstrings, do not comment inline what is obvious
- **Tools** — prefer tool use over CLI and scripts, write ad-hoc test scripts when something becomes too complex

### Try this: generate AGENTS.md from a shared template

You can build `AGENTS.md` from a template, shared standards, and project-specific inputs. This is a good way to bootstrap consistency across repositories:

```text
I want you to generate file AGENTS.md in root folder or completely replace existing one.
- Use this template: #fetch https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/templates/AGENTS.md
- In this project we will use Terraform, extract key insights from https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/standards/TERRAFORM.md
- In this project we will use Python, extract key insights from https://raw.githubusercontent.com/tkubica12/gh-copilot-constitution/refs/heads/main/standards/PYTHON.md
- This project is specifically designed for learning therefore we strive for simplicity.
  - Make sure you do not do complicated and premature abstractions
  - It is OK to start with basic security so users learn fast, but make sure to document next steps for production use cases
  - It is OK to run with simple deployment setup without HA
```

## 2.3 See this first

Open:

- `AGENTS.md`
- `PRD.md`
- `specs\platform\ARCHITECTURE.md`
- `specs\trip\ARCHITECTURE.md`
- `specs\trip\TESTING.md`

What to point out:

- `AGENTS.md` provides the shared default behavior for Copilot and agents
- `PRD.md` captures product goals, scope, and success criteria
- `specs\platform\` holds cross-cutting architecture guidance
- `specs\trip\` and the other service folders show how service-level contracts and delivery expectations are documented

This is the first important workshop message: good agentic work starts with explicit context, not just a clever implementation prompt.

## 2.4 Try this

Start with a safe, read-only discovery question:

```text
/discuss Based on AGENTS.md, PRD.md, and the specs folders, summarize the architecture of this repository, the most important engineering rules, and what constraints a new service should follow. Do not modify files.
```

Then ask:

```text
Which files in specs\platform and specs\trip should I read before changing event-driven messaging, deployment, or testing behavior in this repository?
```

## 2.5 What to observe

- The answer should already reflect rules from `AGENTS.md`.
- Copilot should treat the PRD and specs as first-class context, not as background noise.
- This chapter should feel like architecture and design grounding, not execution yet.

## 2.6 Add spec-driven design to the story

This repository already demonstrates the output of spec-driven work through `PRD.md` and `specs\`. It is also useful to show how that style can be bootstrapped or evolved with shared constitutions and spec tooling.

Key references to explain:

- your shared constitution approach in [gh-copilot-constitution](https://github.com/tkubica12/gh-copilot-constitution)
- `specs\platform\` for project-wide decisions
- `specs\<service>\` for service-specific architecture, security, testing, deployment, and runbooks

If you want to show spec-kit from scratch, this is a good compact flow:

```text
uvx --from git+https://github.com/github/spec-kit.git specify init my_new_project
code my_new_project
/speckit.constitution Create principles focused on clarity, simplicity, speed of development
/speckit.specify Build application that allows people to share ideas using sticky notes with persistent layout and export options
/speckit.plan Frontend is Vite with minimal libraries. Backend is Python and stores sticky note content and spatial layout.
/speckit.tasks
```

The value to explain is not only the tool itself. It is the discipline: write down intent, constraints, contracts, and architecture before asking agents to implement.

## 2.7 Add Copilot Spaces to the context story

Copilot Spaces fit naturally here because they extend planning context beyond a single repo.

Open:

- `.vscode\mcp.json`

What to point out:

- the GitHub MCP server in this workspace enables the `copilot_spaces` toolset through headers
- Spaces are useful for multi-repo planning, PRD shaping, architecture discussions, and issue/project preparation
- this is a strong bridge between high-level planning and the more implementation-focused chapters later

Try:

```text
What are common errors when automating email processing? #list_copilot_spaces #get_copilot_space
```

## 2.8 Why this chapter matters

The audience should leave this chapter with one clear mental model:

> Copilot works better when repository instructions, product intent, specifications, and shared planning context are defined up front.

---


---

Previous: [Course map](00-course-map.md) | Next: [Skills and MCP](02-skills-and-mcp.md)
