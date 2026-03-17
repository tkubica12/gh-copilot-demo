# MCP and approval-aware workflow

## Scenario goal

This scenario shows an agent using tools responsibly: discover capabilities, do read-only work first, pause at an approval boundary, then continue with a clear plan.

## Local MCP setup

The repo already contains a small MCP server in `mcp\random_string_mcp`.

```pwsh
cd C:\git\gh-copilot-demo\mcp\random_string_mcp\src
uv run main.py
```

That server exposes lightweight tool behavior that is easy to understand and easy to extend:

- `random_string(...)`
- `unique_string(...)`

## Copy-paste workflow prompt

```text
You are a workflow agent helping with a demo environment update.

Business goal:
- Prepare a safe rollout plan for a new demo environment called `workshop-agents`.
- Use available tools and MCP integrations where helpful.

Execution policy:
1. Start with discovery only.
   - Inspect `examples\terraform`, `examples\kubernetes`, and `mcp\random_string_mcp`.
   - List which actions are read-only versus mutating.
2. If an MCP server is available, use it only for a low-risk helper task such as generating deterministic suffixes or labels.
3. Before any mutating step, stop and produce an approval summary with:
   - planned action,
   - affected paths,
   - rollback idea,
   - what you still need approved.
4. After approval, continue with the smallest useful change set.

Deliverables:
- A short discovery summary
- A proposed approval checkpoint
- A post-approval execution plan
```

## Sample approval checkpoint

```text
Approval checkpoint

Planned action:
- Add a deterministic environment suffix for `workshop-agents` using the MCP `unique_string` tool.
- Apply the suffix consistently in Terraform and Kubernetes demo assets.

Read-only work completed:
- Reviewed `examples\terraform`
- Reviewed `examples\kubernetes`
- Reviewed `mcp\random_string_mcp\src\main.py`

Mutating work not yet performed:
- No infrastructure files changed
- No deployment command executed

Rollback idea:
- Revert the demo-only naming updates in a single commit if the generated suffix is not wanted.

Approval needed:
- Confirmation to edit demo IaC files
- Confirmation that deterministic suffixes are acceptable for the workshop story
```

## Why this pattern matters

- This example is intentionally simple: approval-aware behavior matters even when the tool itself is trivial.
- The key idea is that the agent separates discovery from action instead of blurring them together.
- In a richer environment, the same pattern can be reused with more capable MCP servers.
