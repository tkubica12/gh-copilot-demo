[Workshop index](README.md) | [Repository README](..\..\README.md)

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


---

Previous: [VS Code agents](03-vscode-agents.md) | Next: [Token efficiency](05-token-efficiency.md)
