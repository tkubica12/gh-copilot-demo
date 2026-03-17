# Agent examples

This folder contains practical orchestration patterns for coordinating multiple agents on bounded work streams instead of relying only on single-turn prompting.
Each example is written to be copied into a CLI-based agent, adapted to a specific customer scenario, and used with the assets already in this repository.

## Suggested exploration order

1. `01-cli-orchestration-and-handoff.md` shows a lead agent splitting work across parallel specialists.
2. `02-mcp-and-approval-aware-workflow.md` shows tool use, approval gates, and workflow-aware behavior.
3. `03-long-running-agent-pattern.md` shows checkpointing, resumability, and background progress patterns.
4. `parallel-work-items.json` provides a seed work queue that an orchestrator can pick up immediately.

## Why these examples exist

- Teams increasingly need practical multi-agent stories.
- Customers want patterns for parallel work, handoff, and approval-aware execution.
- The examples should be concrete enough to feel real without becoming a large reference implementation.

## Repo assets referenced by the examples

- `examples\perftest`
- `examples\kubernetes`
- `examples\terraform`
- `mcp\random_string_mcp`
- `test.http`

The prompts intentionally stay lightweight so teams can trim or expand them for their own environments.
