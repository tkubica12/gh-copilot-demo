[Workshop index](README.md) | [Repository README](../../README.md)

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

- `.github\workflows\issue-triage.md`
- `examples\gh-aw\README.md`
- `examples\gh-aw\issue-triage.md`
- `examples\gh-aw\daily-maintainer-report.md`
- `examples\gh-aw\governance-after-pr.md`

### Issue triage

This is the most concrete and lowest-risk workflow-agent demo. The runnable workflow source lives in `.github\workflows\issue-triage.md`; the matching copy in `examples\gh-aw\issue-triage.md` remains available for discussion with the other examples. After `gh aw compile` generates the `.lock.yml`, the workflow runs when an issue is opened or reopened, classifies the issue with a small allowlist of labels, and posts a short comment about feasibility, clarity, missing details, and the recommended next step.

This maps directly to the latest GitHub Agentic Workflows examples: issue triage is useful because it is judgment-driven, repository-specific, and hard to capture as deterministic YAML. It is also safe to demonstrate because the only writes are `add-labels` and `add-comment`; the agent cannot close the issue, assign users, merge code, or create an implementation PR.

Good live-demo issue comment shape:

```text
Classification: documentation
Feasibility: clear enough for a small docs PR
Missing details: none
Recommendation: assign to Copilot coding agent or handle as a quick maintainer PR
```

### Daily maintainer report

This workflow runs on a weekday schedule. It asks the agent to analyze recent pull requests, failed Actions runs, stale issues, documentation gaps, and security follow-ups — then creates a GitHub issue with a brief, actionable maintainer report. The safe-output configuration limits it to creating issues with a specific title prefix and label set.

### Governance follow-up after pull request

This workflow triggers on pull request events. It asks the agent to summarize the PR intent, highlight unresolved review concerns, note failing CI checks and security findings, and recommend whether the next step should be a coding-agent task, a workflow-agent task, or human review. Again, the only permitted write action is creating a governance issue.

These examples show the pattern: the agent brings judgment and context synthesis, while deterministic pipelines remain the source of truth for builds, tests, and releases.

The three examples form a clear maturity ladder:

| Stage | Example | Safe outputs |
| --- | --- | --- |
| Start | Issue triage | add allowed labels and one comment |
| Scale | Daily maintainer report | create a bounded report issue |
| Govern | Governance after PR | create a bounded follow-up issue |

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
- issue triage is the fastest way to show visible, useful agentic workflow output
- safe outputs make the demo credible because writes are allowlisted and bounded
- human approval and deterministic pipelines still matter

---


---

Previous: [Governance, review, security, and hooks](06-governance-review-security-hooks.md) | Next: [Operations](08-operations.md)
