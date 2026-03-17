# CLI orchestration and handoff

## Scenario goal

This scenario shows a lead CLI agent delegating parallel work, collecting structured handoffs, and turning the outputs into one coherent plan.

## Why this pattern matters

This pattern moves beyond "ask one big prompt" and shows how an orchestrator can manage focused specialists.

## Copy-paste kickoff prompt

```text
You are the orchestrator for a short repo investigation.

Goal:
- Prepare a demo-ready summary of how this repo could support an image-processing workshop story.
- Use parallel specialists instead of doing every step yourself.

Create and manage these workstreams in parallel:
1. Perf specialist
   - Inspect `examples\perftest` and `test.http`
   - Summarize what is already usable for a load or soak demo
   - Identify one lightweight improvement idea
2. Platform specialist
   - Inspect `examples\kubernetes` and `examples\terraform`
   - Summarize what is already demoable for deployment and scale-out conversations
   - Call out one likely customer question
3. MCP specialist
   - Inspect `mcp\random_string_mcp`
   - Explain what tool capability it exposes and how it could fit into a larger workflow

Operating rules:
- Run the specialists in parallel when your tool allows it.
- Require each specialist to return a handoff packet with:
  - `summary`
  - `files_inspected`
  - `demo_value`
  - `open_questions`
  - `next_best_action`
- Do not edit files.
- After collecting handoffs, produce:
  1. a merged summary,
  2. a recommended demo order,
  3. the top 3 follow-up changes to make later.
```

## Handoff prompt for a downstream agent

This handoff template helps one specialist pass clean context to another instead of starting over.

```text
You are receiving a handoff from another agent.

Upstream packet:
- Area reviewed: `examples\perftest`
- Summary: The repo already includes a Dockerfile, a script, and a sample image that can anchor a performance narrative.
- Files inspected:
  - `examples\perftest\Dockerfile`
  - `examples\perftest\script.js`
  - `test.http`
- Demo value: Good setup for showing repeatable API traffic against an image-processing workflow.
- Open questions:
  - Which service should be treated as the primary target in the demo?
  - Should the story focus on throughput, resilience, or cost?

Your task:
- Extend this handoff by connecting it to the deployment story in `examples\kubernetes`.
- Do not repeat the upstream inspection work.
- Produce only the missing context:
  - deployment implications,
  - scaling assumptions,
  - one practical discussion point.
 ```

## What to notice

- Emphasize that the orchestrator is managing scope, not just generating text.
- Highlight the shape of the handoff packet; that structure is often more valuable than the raw prose.
- The same pattern still works with fewer specialists when the scope is smaller.
