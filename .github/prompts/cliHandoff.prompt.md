---
name: cliHandoff
description: Prepare a task for a Copilot CLI background session.
agent: planner
---
Prepare this task for handoff into GitHub Copilot CLI.

Return:

1. recommended isolation mode: workspace or worktree
2. whether to stay interactive, use plan mode, or use autopilot
3. whether `/allow-all` or `/yolo` is appropriate and why
4. whether `/fleet` is useful
5. the exact kickoff prompt
6. a short validation checklist for the presenter

Do not edit files.
