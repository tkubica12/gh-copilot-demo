---
on:
  issue:
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
## Issue Triage

Analyze the triggering issue and help maintainers decide what should happen next.

## What to do

1. Classify the issue by adding one or two allowed labels.
2. Add a short maintainer-facing comment that includes:
   - why the label or labels were selected
   - whether the issue is clear enough for an agent or human to start
   - any missing acceptance criteria, reproduction details, screenshots, logs, or scope decisions
   - a recommendation: coding agent, workflow agent, human review, or close/merge with an existing issue

## Guardrails

- Do not close issues.
- Do not assign users.
- Do not create implementation pull requests from triage.
- If the issue is ambiguous, label it `question` and ask for the smallest missing detail.
- If the issue is actionable and low risk, mention that it is a candidate for assigning to Copilot coding agent.
- Keep the comment concise and useful; avoid generic "thanks for reporting" filler.
