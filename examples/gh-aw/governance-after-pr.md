---
on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:
permissions:
  contents: read
  pull-requests: read
  issues: read
  actions: read
  security-events: read
safe-outputs:
  create-issue:
    title-prefix: "[pr-governance] "
    labels: [copilot, governance, pr]
    close-older-issues: false
---
## Governance Follow-up After Pull Requests

Analyze the triggering pull request and create a governance-focused issue for maintainers.

## What to include

- summary of the PR intent in plain language
- notable review discussion or unresolved concerns
- failing or suspicious CI checks
- relevant security findings or expected follow-up
- whether another coding-agent task, workflow-agent task, or human review is the best next step

## Expectations

- keep deterministic validation as the source of truth
- do not pretend the workflow replaces review or release approvals
- give maintainers a crisp decision-oriented summary
