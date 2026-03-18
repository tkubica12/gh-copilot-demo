# Enterprise demo flow

>> SLIDE: GitHub Enterprise and GitHub Copilot platform overview

## 1. Open with fast wins, but keep them brief

- Next-edit suggestion and autocomplete in VS Code
- A quick codebase understanding prompt grounded in this repository
- Optional short model-selection discussion, but do not let it dominate the session

Goal: establish familiarity, then move quickly to the real story.

## 2. Explain the customization layers before the agent story

- `AGENTS.md` as the always-on repository contract
- Prompt files as reusable one-off workflows
- Custom agents as persistent specialist personas
- Hooks as deterministic policy and audit guardrails
- Skills as packaged local capabilities
- MCP as the bridge to external systems and live tools

This section gives the audience the vocabulary needed for the rest of the demo.

## 3. Move into VS Code custom agents

- Show the `planner` agent and create a plan for the signature scenario
- Use handoff to move into `integration-specialist`
- Use handoff again for `deployment-specialist`
- Explain that `researcher` and `implementer` exist as focused helper subagents

Key message:

- prompt files start work consistently
- custom agents keep a persona active
- subagents narrow scope and reduce context clutter

## 4. Continue in Copilot CLI

- Hand off from VS Code into Copilot CLI
- Show workspace vs worktree isolation
- Use plan mode first, then autopilot only when the task is well-scoped
- Explain `/yolo` accurately as allow-all permissions, not as a separate execution mode
- Show `/tasks`, `/resume`, and `/session`
- If useful, show `/fleet` for independent parallel tasks

This is one of the strongest moments in the live demo because it connects IDE planning to autonomous background execution.

## 5. Go from coding agents to governed delivery

- Create or discuss the PR path
- Use Copilot code review
- Show how security findings, code scanning, or autofix fit after implementation
- Enable the repository hook toggle only when you are about to demonstrate deterministic policy, then disable it again afterward
- Reinforce that humans remain the decision makers

## 6. Add GitHub Agentic Workflows (`gh-aw`)

- Introduce `gh-aw` as additive automation inside GitHub Actions
- Explain markdown workflow source plus compiled `.lock.yml`
- Explain safe outputs, sandboxing, and security-first design
- Use example workflows from `examples\gh-aw`
- Position workflow agents as the next layer after interactive coding agents:
  - summarize repo health
  - triage PR follow-up
  - create governance issues for maintainers

Key message:

- deterministic CI/CD is still the backbone
- workflow agents augment it with Continuous AI

## 7. End on SRE and operations

- Once code is merged and deployed, the story is not over
- Show the value of Azure SRE Agent or similar operational agents
- Connect deployment changes, telemetry, incidents, and remediation

This is the best closing frame because it shows a full software lifecycle, not just code generation.

## 8. Optional extensions if time allows

- documentation generation
- KQL and SQL prompting
- vision and image-to-code
- web search and targeted fetch
- MCP deep dives
- Spark

Use these only when the audience explicitly wants them or when you need a fallback branch.
