[Workshop index](README.md) | [Repository README](..\..\README.md)

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


---

Previous: [Token efficiency](05-token-efficiency.md) | Next: [Workflow agents](07-workflow-agents.md)
