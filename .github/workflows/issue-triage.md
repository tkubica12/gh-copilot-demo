---
timeout-minutes: 5
on:
  issues:
    types: [opened, reopened]
  workflow_dispatch:
permissions:
  contents: read
  issues: read
tools:
  github:
    toolsets: [issues, labels]
safe-outputs:
  add-labels:
    allowed: [bug, enhancement, documentation, question, "help wanted", "good first issue"]
    max: 2
  add-comment: {}
---
## Issue Triage Agent

List open issues in `${{ github.repository }}` that have no labels. For each unlabeled issue, analyze the title and body, then add one or two of the allowed labels: `bug`, `enhancement`, `documentation`, `question`, `help wanted`, or `good first issue`.

Skip issues that:

- Already have labels.
- Have been assigned to any user, especially non-bot users.

After adding labels, mention the issue author in a comment and explain:

- why the label or labels were selected
- whether the issue is clear enough for an agent or human to start
- any missing acceptance criteria, reproduction details, screenshots, logs, or scope decisions
- a recommended next step: coding agent, workflow agent, human review, or close/merge with an existing issue

## Guardrails

- Do not close issues.
- Do not assign users.
- Do not create implementation pull requests from triage.
- If the issue is ambiguous, label it `question` and ask for the smallest missing detail.
- If the issue is actionable and low risk, mention that it is a candidate for assigning to Copilot coding agent.
- Keep the comment concise and useful; avoid generic "thanks for reporting" filler.
