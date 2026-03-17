# Long-running agent pattern

## Scenario goal

This scenario shows how to run a longer task without losing control: maintain a work queue, checkpoint progress, and make handoff or resume easy.

## Why this pattern matters

This pattern matters when work outlasts a single prompt or needs periodic review.

## Copy-paste kickoff prompt

```text
You are a long-running delivery agent working through a small repo backlog.

Primary objective:
- Improve the agent-demo story in this repository using only the tasks in the provided work queue.

Use `examples\agents\parallel-work-items.json` as the source of truth.

Working style:
- Start by restating the queue in priority order.
- Execute one high-value task at a time unless two tasks are explicitly marked as parallel-safe.
- After every completed task, write a checkpoint that includes:
  - completed item IDs,
  - current item,
  - files touched,
  - decisions made,
  - remaining risks.
- If you hit a blocking approval or missing dependency, stop and emit a handoff packet instead of guessing.
- Keep summaries concise enough that another agent can resume from the latest checkpoint.

Success criteria:
- The queue state is always explicit.
- Another agent can take over using only the latest checkpoint plus the work queue file.
- The final summary distinguishes completed work from deferred work.
```

## Suggested checkpoint format

```text
Checkpoint 2

Completed items:
- perf-story
- mcp-suffix-plan

Current item:
- handoff-demo

Files touched:
- examples\agents\01-cli-orchestration-and-handoff.md
- examples\agents\02-mcp-and-approval-aware-workflow.md

Decisions made:
- Keep examples prompt-first and demo-oriented
- Use repo-relative paths so the prompts stay easy to reuse

Remaining risks:
- No automated validation for prompt quality
- The final wording may still need small adjustments for a specific toolchain
```

## Resume prompt

```text
Resume from the latest checkpoint only.

Rules:
- Do not repeat already completed items unless the checkpoint says they are blocked or invalidated.
- Confirm the next active work item.
- Continue using the same queue file and checkpoint format.
- If you detect drift between the queue and the repo, report it before changing files.
```

## What to notice

- This example pairs well with an explanation of background agents, scheduled reviews, or human approval gates.
- The point is not just "run longer"; it is "stay resumable and inspectable while running longer."
