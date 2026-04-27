[Workshop index](README.md) | [Repository README](../../README.md)

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


---

Previous: [Skills and MCP](02-skills-and-mcp.md) | Next: [Copilot CLI](04-copilot-cli.md)
