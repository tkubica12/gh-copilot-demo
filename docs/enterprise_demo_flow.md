# Enterprise scenarios and exploration path

This document maps practical enterprise scenarios that connect the repository assets to the broader GitHub Copilot platform story.

## 1. Foundation: fast wins and platform framing

The opening story is simple:

- GitHub Copilot is now best understood as an agentic engineering platform, not just autocomplete.
- Fast assistive features still matter because they are the easiest entry point into the broader workflow story.
- Model openness and model choice matter more as work moves from quick help to deeper reasoning.

Representative examples:

- a quick TAB or next-edit win in the code editor
- a short repository question that produces a concrete answer
- a small prompt that reveals how context changes output quality

## 2. Copilot Chat Enterprise scenarios

This section focuses on discovery, reasoning, and connected context.

Example prompts and scenarios:

- "I am creating a new project to implement an SDK for our public APIs and publish it for the general public. What license should I pick: Apache, GPL, or MIT?"
- "What does the worker in this repository do?"
- attach a screenshot of a company homepage and ask for a short UX assessment

Connected extension scenarios:

- `@azure /resources Do I have any Azure Container Apps deployed?`
- `@azure /help I created an NSG to filter traffic, but it is still passing.`
- `@azure /costs What can you tell me about storage costs in my subscription?`
- custom extension examples such as `@tomaskubica-gh-extension test`

## 3. Agentic delivery in VS Code and Copilot CLI

This section connects interactive editing to more autonomous execution.

Repository-backed scenarios:

- update the processing API path to `/api/v1/process` across code, docs, and tests
- add dark mode, then extend it into contrast and colorful modes in the frontend
- use Copilot CLI for bounded work with model choice, automation flags, and worktree-based isolation

What this section illustrates:

- editor workflows and terminal workflows are complementary
- specialized agents and stronger context management make longer tasks practical
- local, background, and cloud handoff patterns are part of one delivery system

## 4. Development cycle, review, and DevSecOps

This section connects implementation work to review, scanning, and deployment.

Repository-backed scenarios:

- make a change in `api-processing`, then generate a commit message and pull request summary
- use Copilot-assisted code review in VS Code
- examine findings from Dependabot, CodeQL, OSS supply-chain alerts, or Sonar, then apply Copilot Autofix where appropriate
- inspect failed Actions runs and use Copilot to explain the error

Governance and deployment themes:

- CI and CD remain explicit, including build and Azure Container Apps deployment stages
- Azure VNET-integrated managed agents and workload identity federation fit naturally into the enterprise deployment story
- workflow-agent examples such as `demo-agentic-pr-review.yml` and `demo-agentic-release-readiness.yml` demonstrate markdown-authored briefs, evidence-based automation, and visible guardrails

## 5. Agent HQ, workspaces, and orchestration

This section focuses on coordinated agent work across surfaces.

Key areas:

- Agent HQ or mission control as the orchestration layer across GitHub, VS Code, mobile, and CLI
- GitHub Agentic Workflows in Actions as governed automation with inspectable briefs and guardrails
- workspace-style flows for issue analysis, brainstorming, code generation, and implementation planning
- GitHub Spark as a text-to-code entry point connected to broader engineering workflows

## 6. Modern agent operations

The final section connects the platform capabilities into one operating model.

- VS Code agent mode supports the tightest local edit-run-fix loop.
- Copilot CLI supports terminal-native work with `/model`, built-in agents, `/context`, `/tasks`, MCP, and automation flags.
- Background and cloud agents support asynchronous work that ends in a branch or pull request.
- Agent HQ helps assign, steer, and review multiple agent tasks across surfaces.
- Copilot Memory and Copilot Spaces strengthen recurring work, handoff, and shared context.
