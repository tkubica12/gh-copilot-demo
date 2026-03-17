---
on:
  schedule:
    - cron: "0 7 * * 1-5"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
  actions: read
safe-outputs:
  create-issue:
    title-prefix: "[maintainer-report] "
    labels: [copilot, governance, report]
    close-older-issues: false
---
## Daily Maintainer Report

Create a concise but useful daily maintainer report for this repository as a GitHub issue.

## What to analyze

- recent pull requests and review activity
- recently failed or flaky GitHub Actions runs
- open issues that appear stalled or untriaged
- documentation gaps that keep surfacing
- security and governance follow-up that maintainers should not miss

## Expectations

- be additive to deterministic CI/CD, not a replacement for it
- keep the report brief, actionable, and easy for humans to scan
- call out concrete next steps for maintainers
- avoid noise and obvious information dumps
