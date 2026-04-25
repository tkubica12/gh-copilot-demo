# Copilot token efficiency suite example

This is a sanitized example from real local runs with Copilot CLI, OpenTelemetry file export, and one measured iteration per variant. Treat the numbers as repeatable lab evidence, not universal pricing or billing data.

| Comparison | Baseline | Variant | Baseline tokens | Variant tokens | Savings | Other observations |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Always-on instructions | Large multi-domain `AGENTS.md` | Small `AGENTS.md` plus one relevant skill | 336,024 | 196,277 | 41.6% | Moving unrelated always-on rules into on-demand skills saved context in the task that needed only add-on routing. |
| MCP tool surface | 100 verbose direct MCP tools | Search-then-fetch MCP tools | 223,050 | 131,625 | 41.0% | Progressive discovery saved input tokens even though it used more tool calls. |
| Workflow overhead | One small main-agent prompt | Three low-context mini-model shards | 245,034 | 842,330 | -243.8% | Sharding small work repeated startup/context overhead and cost more. |
| Large-context sharding | One large accumulated-context prompt | Three focused mini-model shards | 478,557 | 1,626,558 | -239.9% | Even with large docs, three separate CLI calls cost more in this harness; delegation needs compression or real isolation to pay off. |
| Compression simulation | Full simulated turn history | Compressed handoff summary | 626,190 | 258,744 | 58.7% | This models `/compact` or a main agent handing a subagent only distilled state. |
| Prompt efficiency | Verbose open-ended prompt | Scoped files and five-bullet output contract | 380,588 | 259,028 | 31.9% | The concise prompt reduced turns, tools, latency, and observed tokens. |

## Takeaways

1. Scoped prompts, progressive MCP discovery, dynamic skill loading, and compression produced measurable savings in this run.
2. Multi-agent sharding did not save tokens when implemented as several independent CLI calls; repeated startup and shared context dominated.
3. The compression case supports the subagent intuition: delegation is economical when the main agent sends a compact handoff instead of accumulated history.
4. Repeat runs and compare quality before converting any single result into a policy.
