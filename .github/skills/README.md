# Skills in this demo

Skills are the repository-local, reusable playbooks for GitHub Copilot.

## How to think about the layers

- `AGENTS.md` sets the default behavior and engineering rules for this repo.
- **Custom agents** specialize roles such as planning, implementation, and review.
- **Skills** package repeatable local guidance, domain context, scripts, or assets that should travel with the repository.
- **MCP** connects Copilot to live external systems and current remote data.

In short: use a skill when the capability should live in the repo; use MCP when the capability depends on a remote system.

## Current skills

- `agent-first-workshop-patterns`: reusable planning, handoff, and orchestration guidance for workshop exercises.
- `json-to-xml-converter`: a script-backed skill with a concrete local utility.
- `simplecontext`: a tiny domain-context skill that demonstrates lightweight, static repository knowledge.

## Adding a new skill

1. Create a folder under `.github/skills/<skill-name>/`.
2. Add `SKILL.md` with frontmatter and concise instructions.
3. Include scripts or templates only when they add real value.
4. Describe when the skill should be used instead of a custom agent or MCP.
