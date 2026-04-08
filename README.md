# GitHub Copilot Demo

This README is the workshop walkthrough. It is written as a **guided learning flow**: each chapter introduces a concept, shows which files to inspect, gives concrete prompts to try, and explains what to observe.

The main story of this workshop is:

1. shape how Copilot works in this repository
2. show packaged capabilities through **skills** and **MCP**
3. move into **custom agents**, **handoffs**, and **subagents**
4. continue execution in **Copilot CLI**
5. govern the result with **review**, **security**, and **hooks**
6. extend the story into **workflow agents** and finally **operations**

This repository is for demonstrations and learning, not for production use.

# 1. Whole story at a glance

The workshop follows one connected engineering story:

- [**Shape Copilot behavior with repository context**](#2-shape-copilot-behavior-with-repository-context) — how Copilot is guided by repository instructions, product intent, specifications, and shared planning context.
- [**Skills and MCP**](#3-skills-and-mcp-local-capabilities-and-connected-tools) — how Copilot gains capabilities through packaged local skills and connected tools.
- [**Plan and specialize work in VS Code**](#4-plan-and-specialize-work-in-vs-code) — prompt files, custom agents, handoffs, and subagents working together.
- [**Continue execution in Copilot CLI**](#5-continue-execution-in-copilot-cli) — plan mode, execution, review, research, session history, and a broad ecosystem of execution surfaces and shared memory.
- [**Govern delivery with review, security, and hooks**](#6-govern-delivery-with-review-security-and-hooks) — code generation is not the end; add cross-model review with the Critic agent.
- [**Add workflow agents in GitHub Actions**](#7-add-workflow-agents-in-github-actions) — repository automation after merge.
- [**Operate with SRE agents**](#8-operate-with-sre-agents) — closing the loop with operational thinking and OpenTelemetry observability.


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

# 3. Skills and MCP: local capabilities and connected tools

This chapter explains how Copilot gains capabilities in two different ways.

## 3.1 Concepts to explain first

Skills and MCP are both useful, but they solve different problems.

| Capability type | Best use |
| --- | --- |
| **Skills** | Easy-to-author, easy-to-share local capabilities, often stored in the repo and loaded on demand |
| **MCP** | Centrally managed, secure, enterprise-grade tools that connect to live systems or remote knowledge |

Good short explanation:

- skills excel when you want something lightweight, local, and easy to package with the repository
- MCP excels when you want live tools, external systems, or centrally managed enterprise integrations

## 3.2 See skills in action

Open:

- `.github\skills\simplecontext\SKILL.md`
- `.github\skills\json-to-xml-converter\SKILL.md`
- `examples\json\myjson.json`

### Try this: lightweight context skill

Ask:

```text
What is inventory number for BigDog?
```

### What to observe

- The model should recognize that the request matches the `simplecontext` skill.
- The detailed skill content is loaded only when needed.
- If your environment exposes tool traces or debug view, you can show the skill file being accessed.

### Try this: script-backed skill

Add `examples\json\myjson.json` to context and ask:

```text
Convert this to XML.
```

### What to observe

- This skill is a good example of a task that benefits from a deterministic script.
- Skills are not only extra text; they can also provide packaged workflows around scripts and resources.

## 3.3 Start with the MCP server that lives in this repo

Open:

- `.vscode\mcp.json`
- `mcp\README.md`
- `mcp\random_string_mcp\README.md`
- `mcp\random_string_mcp\src\main.py`

Start with the local server because it is transparent and easy to explain.

What to point out:

- `.vscode\mcp.json` registers `my-mcp-string-generator`
- it connects to `http://localhost:8000/sse`
- `mcp\random_string_mcp\src\main.py` is a tiny FastMCP server
- the server exposes two tools: `random_string` and `unique_string`
- this is a great teaching example because the audience can see both the tool registration and the implementation

### How this MCP server is built

`random_string_mcp` uses `FastMCP` and exposes Python functions as MCP tools with the `@mcp.tool()` decorator.

- `random_string(...)` generates a random suffix from the selected character classes
- `unique_string(...)` derives a predictable suffix from a seed using SHA-256, which is useful when you want stable names
- `mcp.run(transport="sse")` starts the server over Server-Sent Events, which is why the workspace configuration uses an HTTP URL

### How to start it

Open a terminal and run:

```pwsh
cd .\mcp\random_string_mcp\src
uv run main.py
```

The workspace MCP configuration points Copilot to `http://localhost:8000/sse`, so once the server is running the tool becomes available in chat.

### Try this

Use the earlier demo prompt:

```text
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers.
```

Then show a second prompt that highlights deterministic behavior:

```text
Generate stable suffixes for dev, test, and prod using the unique string tool so that the same environment names always produce the same suffixes.
```

### What to observe

- this is a real MCP server that lives in the repository, not only a hosted enterprise integration
- the implementation is simple enough that students can understand how custom MCP tools are authored
- the random generator is useful for one-off names, while the unique generator is useful for repeatable naming patterns

## 3.4 Connect to broader MCP servers

After the local example, notice the configured servers such as:

- GitHub MCP
- Microsoft Docs MCP
- Kubernetes MCP
- Azure MCP Server

### Try this: official docs through MCP

Ask:

```text
Using the Microsoft Docs MCP server, find official guidance on custom agents in VS Code and summarize how handoffs work.
```

### Try this: repository knowledge through GitHub MCP

Ask:

```text
Using GitHub tools, list the workflows in this repository and summarize which ones are build, deploy, or security related.
```

### Optional follow-up prompts

If your environment supports these integrations, try:

```text
What plans we have for implementing PDF in our app? Check GitHub Issues.
```

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

## 3.5 Why this chapter matters

The audience should now understand the difference between:

- local packaged capabilities
- repository-local MCP tools you can build yourself
- centrally connected tools

That distinction becomes important in the later chapters.

---

# 4. Plan and specialize work in VS Code

This chapter is where the main workflow becomes more agentic.

## 4.1 Concepts to explain first

This chapter introduces four related ideas:

| Concept | Best use |
| --- | --- |
| **Prompt file** | Start a workflow in a consistent way |
| **Custom agent** | Keep a specialist role active |
| **Handoff** | Move the conversation from one specialist role to another while keeping context |
| **Subagent** | Delegate a narrower, focused job without cluttering the main conversation |

The key learning goal here is:

> a prompt file can initiate a workflow, a custom agent can carry the role, a handoff can move between roles, and a subagent can narrow scope even further.

## 4.2 See this first

Open:

- `.github\prompts\workshopPlan.prompt.md`
- `.github\agents\planner.agent.md`
- `.github\agents\integration-specialist.agent.md`
- `.github\agents\deployment-specialist.agent.md`
- `.github\agents\researcher.agent.md`
- `.github\agents\implementer.agent.md`

## 4.3 Start the workflow from a prompt file

Use:

```text
/workshopPlan Create a step-by-step plan for modernizing the event-driven platform slice in this repository. Focus on examples/terraform, .github/workflows, hooks, and workflow automation. Do not edit files yet.
```

### What to observe

- A prompt file started the workflow.
- That prompt also routed the conversation into the `planner` custom agent.

## 4.4 Continue with handoff to specialists

Use handoff to continue into `integration-specialist`.

If you prefer to type a direct prompt, use:

```text
Use the integration-specialist agent to identify which repo files define the current Service Bus, container app, and worker flow, summarize the change surface, and propose the smallest safe implementation slice.
```

Then continue into `deployment-specialist`:

```text
Use the deployment-specialist agent to review Terraform, GitHub Actions, hooks, and workflow-agent assets that should change together for this scenario.
```

### What to observe

- Each agent has a different role and different emphasis.
- Handoffs help keep the workflow structured rather than mixing all concerns into one conversation.

## 4.5 Create a custom agent live

After showing the prebuilt agents in the repository, create one from natural language so the audience sees that custom agents are not only hand-authored files.

Use:

```text
/create-agent This agent is specialized for business analytics, interactively gathers requirements, asks clarifying questions and outputs PRDs
```

If Copilot asks follow-up questions, answer in a way that broadens the scope slightly beyond pure dashboards. A good workshop answer is:

```text
Analytics plus broader product PRDs. Keep it lightweight and business-facing, but proactive about KPIs and reporting requirements.
```

### What to observe

- `/create-agent` turns a plain-language specialization request into a reusable `.agent.md`.
- Copilot does not need a perfect specification upfront; it can draft, identify ambiguity, and iterate.
- This is a strong example of taking a repeated working style from chat and turning it into a durable specialist.
- The final artifact is still just a file, so teams can review, version, and refine it like any other repository asset.

## 4.6 Explain subagents

Now show:

- `.github\agents\researcher.agent.md`
- `.github\agents\implementer.agent.md`

Explain:

- the main specialist agent keeps the broad task in mind
- a subagent can take on a narrower job with a tighter context
- this reduces context clutter and makes orchestration easier

You do not need to force visible subagent execution every time. It is enough to explain the pattern and show how it is defined in the repo.

## 4.7 Why this chapter matters

This is the chapter where students usually see the real difference between:

- plain chat prompting
- reusable workflow design
- multi-agent engineering

---

# 5. Continue execution in Copilot CLI

This chapter moves from IDE planning into autonomous execution.

## 5.1 Concepts to explain first

Copilot CLI is important because it makes the workflow more operational:

- sessions are explicit
- modes are explicit
- background work is explicit
- permissions are explicit

Important terminology:

- **plan mode** is for creating and refining the plan
- **autopilot** is the autonomous execution mode
- **`/yolo`** is an alias for allow-all permissions
- **`/yolo` is not a separate mode**

## 5.2 Start the CLI

Open a terminal and run:

```text
copilot
```

## 5.3 Use plan mode first

Switch to plan mode with `Shift+Tab` and ask:

```text
Create an implementation plan for modernizing the event-driven platform slice in this repository. Focus on examples/terraform, .github/workflows, hooks, and examples/gh-aw. Do not edit files yet.
```

### What to observe

- Copilot CLI is not only for execution; it can also be used as a planning surface.

## 5.4 Continue into execution

After you agree on the plan, continue with:

```text
Now continue the agreed task. Keep changes focused on documentation and workshop assets first so the workflow remains easy to review.
```

If the task is well-scoped and you want to discuss autonomy, explain when autopilot becomes appropriate.

## 5.5 Explain session and task management

Copilot CLI sessions persist locally in `~/.copilot/session-state/`. You can pick up any previous session, rename it for clarity, and manage background tasks.

Use and discuss:

```text
/tasks
/session
/resume
/rename
/compact
```

### Try this

Resume a previous session with the session picker:

```text
/resume
```

The picker groups sessions by branch and repository. Select a session and continue where you left off. Then rename it:

```text
/rename Modernize event-driven slice
```

### What to observe

- `/resume` works for both local CLI sessions and cloud coding agent sessions — you can resume a cloud session locally
- `/rename` makes it easy to find sessions later when you have many
- `/compact` compresses conversation history so long-running sessions never hit context limits (auto-compaction also runs at 95% of the context window)

## 5.6 Review, diff, and share work

Before opening a pull request, the CLI has built-in tools to inspect what changed and share it with others.

| Command | What it does |
| --- | --- |
| `/diff` | Review all changes made during the session with syntax-highlighted inline diffs. Toggle between session changes and branch diffs. Add line-specific comments. |
| `/review` | Run the code-review agent on staged or unstaged changes for a quick sanity check before committing. |
| `/share file [PATH]` | Export the session conversation as a Markdown file. |
| `/share gist` | Export the session as a private gist on GitHub. |
| `/share html [PATH]` | Export the session as a self-contained interactive HTML file. |

### Try this

After the earlier execution step, run:

```text
/diff
```

Browse the changes, then run a quick review:

```text
/review
```

Finally, share the session so a colleague can see what you did:

```text
/share gist
```

### What to observe

- `/diff` and `/review` close the gap between generating code and opening a PR — the CLI has governance tooling built in, not just generation
- `/share` makes sessions a first-class artifact that can be handed off, archived, or used for async collaboration
- these commands connect naturally to Chapter 6 (PR review and governance)

## 5.7 Research with the CLI

The `/research` command activates a specialized research agent that gathers information from your codebase, GitHub repositories, and the web. It produces a comprehensive Markdown report with citations — not a quick chat answer.

### Try this

```text
/research How is event-driven messaging implemented in this repository?
```

When the research completes, Copilot shows a summary and a link to the full report. Press `Ctrl+Y` to open the report in your terminal editor. Then share it:

```text
/share file research
```

### What to observe

- research reports are saved to disk as permanent artifacts, not transient chat messages
- the agent searches across your local codebase, organization repositories (if logged in), and the web
- the report format adapts to your query type: process questions get step-by-step guidance, conceptual questions get narrative explanations, technical deep-dives get architecture diagrams and code examples
- the research agent uses a fixed model (not configurable via `/model`)

## 5.8 Chronicle: session insights and self-improvement

The `/chronicle` command turns your CLI session history into actionable insights. It reads the local session store to generate standup reports, personalized tips, and suggestions for improving your custom instructions.

**Note:** `/chronicle` is an experimental feature. Enable it first:

```text
/experimental on
```

| Subcommand | What it does |
| --- | --- |
| `/chronicle standup` | Summarize recent work including branch names, PR links, and status checks |
| `/chronicle tips` | Personalized tips for using the CLI more effectively based on your actual usage patterns |
| `/chronicle improve` | Analyze session history for friction patterns and generate custom instructions to reduce them |
| `/chronicle reindex` | Rebuild the session store from session files on disk |

### Try this

```text
/chronicle standup last 3 days
```

Then:

```text
/chronicle tips
```

### What to observe

- this is a feedback loop: Copilot uses your real session history to help you work better
- `/chronicle improve` is particularly powerful — it finds patterns where Copilot misunderstood your intent and generates custom instructions to fix them
- all session data stays local in `~/.copilot/session-state/` — nothing is uploaded beyond normal model interactions
- you can also ask free-form questions about past work, like "Have I worked on anything related to the payments API?"

## 5.9 Explain parallelism

If you want to show fan-out work, use `/fleet` for clearly separable tasks.

Example:

```text
Research this repository in parallel: one agent should inspect Terraform and deployment workflows, another should inspect hooks and workflow-agent examples, and another should summarize how the workshop story should flow for students.
```

## 5.10 Execution surfaces, Copilot Memory, and third-party agents

This is an important teaching moment. Copilot offers multiple ways to run coding agents, and understanding the full landscape helps teams choose the right surface for each task.

### Execution surfaces

| Surface | How to start | Best for |
| --- | --- | --- |
| **Copilot CLI (local)** | `copilot` in terminal | Interactive work, plan mode, local iteration |
| **Copilot CLI task (background)** | Start from VS Code or CLI | Long-running work in a local worktree |
| **Cloud coding agent (PR-based)** | Assign a GitHub issue to Copilot or use the agents panel | Autonomous work that runs in GitHub's cloud |
| **Third-party agents (Claude, Codex)** | Agents tab, issues, PR comments (`@AGENT_NAME`) | Alternative coding agents with different model strengths |
| **GitHub.com web** | Agents panel on any page, agents tab in repository | Quick tasks, monitoring, session review |
| **GitHub Mobile** | Home view → agent sessions | On-the-go monitoring and task creation |

What to explain:

- from VS Code you can start a Copilot CLI task that runs in the background in a local worktree
- you can also assign a GitHub issue or PR to Copilot and it will work as a cloud coding agent
- **Agent HQ** in VS Code provides a single view of all running and completed agent sessions across local CLI tasks, cloud tasks, and PR-based agents
- the **agents panel** on GitHub.com lets you start and monitor agent tasks from any page without navigating away
- the **agents tab** in a repository shows all agent sessions for that repo, with session logs and one-click PR links
- **GitHub Mobile** shows agent sessions on the Home view, so you can monitor progress on the go

### Copilot Memory

Copilot can develop a persistent understanding of a repository by storing **memories** — tightly scoped pieces of information it deduces while working. This is different from custom instructions: memories are learned automatically, not written manually.

Key concepts:

- memories are **repository-scoped**, not user-scoped — what one developer's session learns is available to all users with memory enabled in that repo
- memories are created with **citations** to specific code locations and are **validated** against the current codebase before use — stale memories are ignored
- memories **auto-delete after 28 days** to prevent outdated information from affecting decisions
- memories work across execution surfaces: what the **cloud coding agent** learns, **code review** and **CLI** can use later
- repo owners can view and delete memories in **Settings → Copilot → Memory**

Enterprise considerations:

- enabled by default for Copilot Pro/Pro+ users
- off by default for org/enterprise-managed subscriptions — admins must enable it
- if a user belongs to multiple organizations, the most restrictive policy wins

### Try this

Show Agent HQ in VS Code (look for it in the Copilot sidebar). If you have a running CLI session or a cloud agent, it should appear there.

If the repository has been worked on by Copilot with memory enabled, show the memories page: open the repository on GitHub → Settings → Copilot → Memory.

Then explain that regardless of whether the agent ran locally or in the cloud, the shared context, session history, and repository memories are available across all surfaces.

### Third-party coding agents

In addition to GitHub's own cloud coding agent, **Anthropic Claude** and **OpenAI Codex** are available as third-party coding agents (public preview). They work the same way:

- assign an issue or give a prompt from the agents tab, an issue, or a PR comment (`@AGENT_NAME`)
- the agent works on the changes and creates a pull request
- review the PR and leave comments to iterate

They consume **GitHub Actions minutes** and **Copilot premium requests**. They must be enabled in account/org policies.

**Note:** Third-party agents are different from the deprecated Copilot Extensions. MCP is now the extensibility model for bringing tools into Copilot.

### Self-hosted runners for cloud agents

Cloud coding agents and Copilot code review run on GitHub Actions runners. By default these are GitHub-hosted, but organizations can use **self-hosted runners** for:

- access to internal resources behind a firewall
- faster performance with larger runners
- networking control and compliance requirements

Self-hosted runners require **ARC** (Actions Runner Controller) and **Ubuntu x64 Linux**. Organization admins can set the default runner and **lock the setting** across all repos so individual repositories cannot override it. Configuration is done through `copilot-setup-steps.yml` or organization-level settings.

## 5.11 Why this chapter matters

This is where the workflow starts to look like real engineering rather than a single conversation. The CLI is not just an execution tool — it reviews changes, researches topics, learns from session history, and connects to a broader ecosystem of execution surfaces, shared memory, and third-party agents.

---

# 6. Govern delivery with review, security, and hooks

This chapter shows that engineering does not end when code is generated.

## 6.1 Open a pull request and use Copilot review in GitHub

The best way to demonstrate code review is directly in the GitHub portal.

Recommended flow:

1. Create a branch with a small but real workshop change.
2. Open a pull request in GitHub.
3. Show the PR summary and the **Files changed** tab.
4. Trigger Copilot review or use the PR review experience in GitHub.
5. Ask Copilot to identify correctness risks, missing validation, and follow-up checks.

If you also want an in-chat parallel to the portal demo, you can still use the `reviewer` custom agent or a direct review prompt.

Example prompt:

```text
Review the proposed changes. Focus on correctness, risk, and what still needs validation.
```

And:

```text
What are the highest-risk parts of this change if it were opened as a pull request?
```

### What to observe

- GitHub is the natural place to show review as part of collaboration, not only generation
- pull request review is where Copilot, human feedback, CI results, and branch policy come together
- this is an ideal bridge from coding agents into governance
- **connect the dots**: if you demonstrated `/review` in the CLI chapter (section 5.6), explain that CLI review and PR-based review are complementary — CLI review catches issues before commit, PR review catches issues before merge

## 6.2 Show security review in the GitHub portal

Explain the repository surfaces that continue the flow:

- the **Security** tab
- code scanning alerts
- dependency findings
- autofix and remediation
- workflow checks in `.github\workflows`

Open these workflow files before or during the demo:

- `.github\workflows\devskim.yml`
- `.github\workflows\ossar.yml`
- `.github\workflows\tfsec.yml`
- `.github\workflows\sonarcloud.yml`

What to explain:

- this repository already contains security-oriented workflows that run on pull requests
- `devskim`, `ossar`, and `tfsec` upload SARIF results into GitHub security surfaces
- security review is stronger when the audience can see the link between PR checks, uploaded findings, and remediation

Example prompt:

```text
Which workflows or security checks are most relevant to validating this kind of change in this repository?
```

If you have a real alert available, show the alert details page and discuss whether Copilot Autofix or remediation guidance is appropriate before merge.

## 6.3 Explain hooks

Hooks are a way to add **deterministic, scripted policy** around Copilot agent behavior. While prompts and custom agents influence behavior probabilistically (the model can choose to follow or not), hooks run real scripts at specific lifecycle events and can enforce hard rules.

Copilot reads hook configuration from `.github\hooks\copilot-policy.json`. In this repository, the file is shipped as `.github\hooks\copilot-policy.json.disabled` so hooks stay fully inactive by default — rename it to activate.

For workshop safety, the hooks in this repository are now **opt-in by default**. They are not registered with Copilot until you explicitly install the demo policy file, so they do not interfere with earlier CLI sections, unrelated repository work, or VS Code preview sessions.

This repository defines three hooks:

| Hook event | What it does in our example |
| --- | --- |
| **sessionStart** | Runs when an agent session begins. Our script shows a policy banner reminding the agent of repository rules. |
| **userPromptSubmitted** | Runs after every user prompt. Our script logs the prompt for audit purposes. |
| **preToolUse** | Runs before the agent executes any tool (shell command, file edit, etc.). Our script inspects the command and **blocks dangerous patterns** such as `rm -rf`, `format`, or force-push. This is the strongest control point because it can reject an action before it happens. |

Open:

- `.github\hooks\copilot-policy.json.disabled`
- `.github\hooks\scripts\session-banner.ps1`
- `.github\hooks\scripts\log-prompt.ps1`
- `.github\hooks\scripts\pre-tool-policy.ps1`

Before this section, create the runtime policy file in a separate terminal and then start a fresh Copilot session if one is already open:

```powershell
Rename-Item .\.github\hooks\copilot-policy.json.disabled copilot-policy.json
```

When you are done with the hooks section, disable the policy file again and start a fresh Copilot session before continuing other demos:

```powershell
Rename-Item .\.github\hooks\copilot-policy.json copilot-policy.json.disabled
```

If `.github\hooks\copilot-policy.json` exists, Copilot invokes the repository hooks. When it is renamed to `.disabled`, there are no repo hooks to run. Audit entries are written to `.github\hooks\logs\audit.jsonl` while the policy file is active.

### Try this

Ask:

```text
Explain what this repository hook configuration does, when each hook runs, and why preToolUse is the strongest control point in this example.
```

### What to observe

- hooks are not AI — they are deterministic scripts that always execute once the runtime policy file is present
- in this repo, they are only registered after you deliberately create the hook policy file
- `preToolUse` can block dangerous operations regardless of what the model wants to do
- this is a natural complement to review and security: probabilistic guidance from instructions and agents, hard enforcement from hooks

Hooks work in Copilot CLI today and VS Code also supports them in preview. For the live demo, treat hooks as **CLI-first** and mention the VS Code support as an additional surface. If you create or remove the hook policy file while VS Code already has an active Copilot chat session, restart that session so it reloads the repository hook policy cleanly.

## 6.4 The Critic agent (Rubber Duck)

The Critic agent — also called **Rubber Duck** — is an experimental feature where a second LLM from a **different model family** reviews the primary agent's plans and implementations before they are presented to you.

When Claude is the orchestrator, Rubber Duck runs on GPT-5.4 (and vice versa). Different model families carry different training biases, so a review from a complementary family surfaces errors that the primary model consistently misses.

**Note:** This feature requires `/experimental on` in the CLI and is currently available for Claude models.

What it catches:

- details the primary agent may have missed
- assumptions worth questioning
- edge cases to consider
- incorrect logic or wrong API usage

GitHub's benchmark on SWE-Bench Pro showed that Claude Sonnet 4.6 paired with Rubber Duck closed **74.7%** of the performance gap between Sonnet and Opus. The benefit is strongest on difficult, multi-file problems.

### What to explain

- this is a governance mechanism built into the agent itself — the agent checks its own work before presenting it to you
- it complements hooks (hard enforcement) and review (human judgment) with automated cross-model validation
- the cost is additional model calls, but for complex tasks the quality improvement is substantial

## 6.5 Why this chapter matters

Students should now see that AI engineering is not only about generation. It is also about:

- control
- governance
- validation

---

# 7. Add workflow agents in GitHub Actions

This chapter extends the story from interactive agents into repository automation.

## 7.1 Concepts to explain first

Traditional GitHub Actions workflows are deterministic YAML pipelines: build, test, deploy. They are excellent at repeatable, well-defined steps. But repositories also have tasks that are judgment-driven, context-heavy, or hard to express as fixed rules — things like triaging a new issue, summarizing what happened in a failed CI run, or creating a governance follow-up after a pull request.

[GitHub Agentic Workflows](https://github.github.com/gh-aw/) (`gh-aw`) solve this by letting you **author workflows in Markdown instead of YAML**. An AI agent receives the repository context and your natural-language instructions, then performs the task inside a sandboxed GitHub Actions runner. The key design principles are:

- **Markdown source** — you describe what you want, not how to script it
- **Compiled lock file** — `gh aw compile` turns the Markdown into a standard `.lock.yml` Actions workflow
- **Safe outputs** — all write operations (creating issues, adding labels, posting comments) go through an explicit allowlist so the agent cannot make uncontrolled changes
- **Read-only by default** — the agent can read the repository but must be granted specific permissions for any writes
- **Additive to CI/CD** — agentic workflows complement deterministic pipelines, they do not replace builds, tests, or release gates

## 7.2 What our examples do

Open:

- `examples\gh-aw\README.md`
- `examples\gh-aw\daily-maintainer-report.md`
- `examples\gh-aw\governance-after-pr.md`

### Daily maintainer report

This workflow runs on a weekday schedule. It asks the agent to analyze recent pull requests, failed Actions runs, stale issues, documentation gaps, and security follow-ups — then creates a GitHub issue with a brief, actionable maintainer report. The safe-output configuration limits it to creating issues with a specific title prefix and label set.

### Governance follow-up after pull request

This workflow triggers on pull request events. It asks the agent to summarize the PR intent, highlight unresolved review concerns, note failing CI checks and security findings, and recommend whether the next step should be a coding-agent task, a workflow-agent task, or human review. Again, the only permitted write action is creating a governance issue.

Both examples show the pattern: the agent brings judgment and context synthesis, while deterministic pipelines remain the source of truth for builds, tests, and releases.

## 7.3 Try this

Ask:

```text
Explain what this GitHub Agentic Workflow would do, what safe outputs it uses, and how it complements deterministic CI/CD instead of replacing it.
```

Then ask:

```text
Draft a variant of this workflow that creates a governance issue only when pull request checks fail or security findings appear.
```

## 7.4 What to observe

- workflow agents are a natural next step after coding agents
- they are useful for scheduled or event-driven repository automation
- human approval and deterministic pipelines still matter

---

# 8. Operate with SRE agents

The workshop should end by showing that the lifecycle continues after merge and deployment.

## 8.1 If your environment supports it, try operational prompts

```text
What versions my AKS clusters run?
```

```text
See my storage accounts, can I improve resiliency and data protection?
```

```text
What namespaces I have in my Kubernetes cluster?
```

## 8.2 What to explain

- operations and SRE agents help after deployment
- they connect code changes, infrastructure, telemetry, and incidents
- they are a strong closing chapter because they complete the lifecycle story

If a dedicated Azure SRE Agent environment is available, this is the ideal final demo. If not, Azure or Kubernetes MCP prompts are still a strong close.

## 8.3 Observe Copilot with OpenTelemetry

Copilot Chat in VS Code and Copilot CLI can export **OpenTelemetry** traces, metrics, and events, giving you visibility into agent interactions, LLM calls, tool executions, and token usage. All signals follow the [OTel GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/).

### What gets collected

| Signal | Examples |
| --- | --- |
| **Traces** | Full span tree: agent orchestration → LLM calls → tool executions. Subagent invocations appear as child spans. |
| **Metrics** | LLM call duration, token usage (input/output), tool invocation count and latency, agent end-to-end duration, time to first token |
| **Events** | Session starts, per-tool invocations, per-turn LLM round-trips |

### How to enable

In VS Code, set `github.copilot.chat.otel.enabled` to `true` and configure the OTLP endpoint. In the CLI, set `COPILOT_OTEL_ENABLED=true` or `OTEL_EXPORTER_OTLP_ENDPOINT`.

Content capture (full prompts and responses) is **off by default** — enable with `captureContent` only in trusted environments.

### Try this

If you have a local observability stack, the fastest option is the **Aspire Dashboard**:

```text
docker run --rm -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

Then configure VS Code:

```json
{
  "github.copilot.chat.otel.enabled": true,
  "github.copilot.chat.otel.exporterType": "otlp-grpc",
  "github.copilot.chat.otel.otlpEndpoint": "http://localhost:4317"
}
```

Open `http://localhost:18888` → Traces to see agent interaction spans.

Other supported backends: Jaeger, Azure Application Insights, Langfuse, Grafana Tempo, Honeycomb, Datadog — any OTLP-compatible backend works.

### Why this matters for enterprise

- **compliance**: audit trail of what the agent did, which tools it called, and what context it used
- **cost management**: token usage metrics help teams understand and optimize AI spend
- **debugging**: trace trees show exactly where an agent interaction went wrong
- **performance**: latency metrics identify slow tool calls or model responses

---

# 9. Optional demos

Not every audience wants the same depth. The chapters above are the main story. The items below are excellent optional branches when you want to go deeper or adapt to a different audience.

## 9.1 Foundations and quick wins

### Inline suggestions

Open `src\services\toy\main.py` and type `# Configure Prometheus` — wait for suggestions. Use TAB to accept, ESC to reject, or CTRL+arrow to accept partially.

Then around line 25 change `logger` to `logging` and wait for Copilot to predict the next edit.

### Chat and codebase understanding

Ask Copilot to search and understand your code:

```text
Where in my code am I processing messages from Service Bus queues and what is the code doing?
```

Experiment with different model selections to compare quality and speed.

### Documentation generation

This is still an excellent demo for many developers because it solves a common day-to-day task quickly.

Add all Terraform files from `examples\terraform` to context and try this sequence:

```text
Create basic Markdown documentation for this Terraform project, explain how to deploy it, and summarize the purpose of each file.
```

```text
Create list of cloud resources used in this project.
```

```text
Create chapter listing environment variables used with each container app and put it into nice table.
```

## 9.2 Structured prompting

### KQL

Attach [query_data.csv](./examples/kql/query_data.csv) and ask:

```text
Give me microsoft Kusto Query (KQL) to display percentage of processor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.
```

### SQL

Attach [users_denormalized.json](./examples/sql/users_denormalized.json) and ask:

```text
Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.
```

Then follow up:

```text
Based on data structure, create 10 lines of sample data and make sure it makes sense and foreign keys are respected.
```

```text
Give me SQL statement to list userId, name, number of orders and number of addresses for each user.
```

### Vision

Attach [classes.png](./examples/vision/classes.png), create `classes.py` and ask:

```text
Generate code for classes in Python according to attached schema.
```

Then in Edit mode follow with:

```text
Create markdown documentation for classes.py and include mermaid diagram.
```

## 9.3 Web and browser demos

### Browser elements

Open Simple Browser (command palette CTRL+ALT+P and search for it), enter some URL. Click on **Add element to chat** and ask `What is this element doing?`

### Web search and fetch

Useful for demonstrating the difference between model-only answers, server-side web grounding, MCP-backed research, and targeted fetch of known documentation.

Try without tools first:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version? Do NOT use any tools.
```

Then with tools enabled:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
```

And with explicit fetch of known documentation:

```text
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
#fetch
https://github.com/microsoft/agent-framework/releases
https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
```

## 9.4 Additional MCP integrations

The main flow already covers the in-repo `random_string_mcp` server and GitHub MCP. If the audience wants more, try:

- Kubernetes MCP
- Azure MCP
- Database MCP
- Playwright MCP

## 9.5 Model selection and BYOM/BYOK

### Model selection basics

Copilot CLI supports model switching during a session with `/model`. Show the model picker and explain the trade-offs:

- **Larger models** (Claude Opus, GPT-5.3-Codex): better for complex, multi-file tasks
- **Faster models** (Claude Haiku, GPT-5 mini, GPT-4.1): better for quick tasks, included at no premium request cost
- **Reasoning models**: toggle reasoning visibility with `Ctrl+T`, configure reasoning effort

### Bring your own model provider

Copilot CLI supports connecting your own model provider or running fully local models. Configure via environment variables before launching the CLI:

- **Remote providers**: Azure OpenAI, Anthropic, OpenAI, or any OpenAI-compatible endpoint
- **Local models**: Ollama, vLLM, Foundry Local
- **Offline mode**: set `COPILOT_OFFLINE=true` to prevent all communication with GitHub servers — fully air-gapped development
- **GitHub auth becomes optional**: when using your own provider, you can start the CLI without GitHub authentication. Sign in to GitHub to also get `/delegate`, GitHub Code Search, and the GitHub MCP server.

Sub-agents (explore, task, code-review) automatically inherit your provider configuration.

### Try this

If you have Ollama running locally:

```text
COPILOT_PROVIDER_BASE_URL=http://localhost:11434 copilot
```

Or show the help for provider setup:

```text
copilot help providers
```

### Enterprise BYOK

For organization-managed Copilot, enterprise BYOK allows admins to connect API keys from supported providers (Anthropic, Microsoft Foundry, OpenAI, xAI). Once connected, all models tied to that key are available in Copilot Chat across GitHub.com and supported IDEs. Usage through BYOK is billed directly by the provider and does not count against Copilot request quotas.

## 9.6 LSP in the CLI

LSP (Language Server Protocol) gives Copilot CLI IDE-like intelligence: go-to-definition, hover information, and diagnostics. This helps the agent navigate your codebase with the same precision as a full IDE.

### Configuration

Configure LSP servers via:

- **Global**: `~/.copilot/lsp-config.json`
- **Repository**: `.github/lsp.json`

Plugins can also contribute LSP servers automatically.

### Managing LSP

```text
/lsp show     # see configured servers
/lsp test     # verify a server works
/lsp reload   # reload configuration
/lsp help     # full documentation
```

### What to explain

- without LSP, the CLI relies on grep and pattern matching for code navigation
- with LSP, it understands types, references, and definitions — making refactoring and cross-module work significantly more accurate
- this is particularly valuable for statically typed languages with complex type hierarchies

## 9.7 Self-hosted runners deep-dive

For enterprise audiences who want more detail on running cloud agents on their own infrastructure:

- cloud coding agents and Copilot code review can run on **self-hosted runners** using ARC (Actions Runner Controller)
- only **Ubuntu x64 Linux** runners are supported
- organization admins can **set a default runner type** and **lock the setting** to prevent individual repos from overriding it
- firewall rules must allow connections to `api.githubcopilot.com`, `uploads.github.com`, and `user-images.githubusercontent.com`
- configuration is done via `copilot-setup-steps.yml` in the repository or organization-level settings

Use cases:

- **internal network access**: agent can reach internal package registries, databases, or APIs
- **performance**: use larger runners for faster builds and tests
- **compliance**: keep agent execution within your own infrastructure
- **cost control**: use reserved compute instead of pay-per-minute GitHub-hosted runners

## 9.8 Future-looking closing topics

- GitHub Spark
