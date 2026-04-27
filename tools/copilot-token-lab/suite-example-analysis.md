# Copilot token efficiency suite example

This is a sanitized example from a real local run with the Python runner, Copilot CLI backend, OpenTelemetry file export, and one measured iteration per variant. Treat the numbers as repeatable lab evidence, not universal pricing or billing data. Cost units use the relative demo rates in `model-pricing.toml`, not official prices. For run-level details, see [reports/python-suite-2026-04-26.md](reports/python-suite-2026-04-26.md).

| Comparison | Baseline | Variant | Baseline tokens | Variant tokens | Total-token result | Output-token result | Cost result | Other observations |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Always-on instructions | Large scaled multi-domain `AGENTS.md` | Small `AGENTS.md` plus one relevant skill | 155,188 | 70,947 | 54.3% saved | 96.4% more | 69.4% saved | Scaling unrelated always-on instructions made the skill-loading advantage visible. |
| MCP tool surface | 100 verbose direct MCP tools | Search-then-fetch MCP tools | 117,171 | 77,859 | 33.6% saved | 144.8% more | 32.2% saved | Progressive discovery saved context even though it used more tool calls and a longer answer. |
| Prompt efficiency | Verbose open-ended prompt | Scoped files and five-bullet output contract | 256,672 | 76,174 | 70.3% saved | 88.6% saved | 72.9% saved | Tight file bounds and output shape reduced turns, tools, latency, and cost units. |
| Compression simulation | Inline simulated turn history | Inline compressed handoff | 84,644 | 75,516 | 10.8% saved | 23.1% saved | 17.9% saved | The inline transcript is capped to stay below Windows command-line limits, so this is a conservative compression demo. |
| Response style | Detailed incident guide | Caveman-inspired terse guide | 45,092 | 74,890 | 66.1% more | 89.4% saved | 31.5% saved | Output dropped from 6,744 to 712 tokens; raw total worsened because cache-read tokens dominated this single run. |
| Workflow overhead | One small main-agent prompt | Three low-context mini-model shards | 56,120 | 186,236 | 231.9% more | 0.0% saved | 26.2% saved | Sharding small work used more tokens but cheaper mini-model rates lowered estimated cost units. |
| Large-context sharding | One large accumulated-context prompt | Three focused mini-model shards | 76,920 | 239,203 | 211.0% more | 3.9% more | 21.5% saved | Separate mini-model calls still repeated context, but price-aware routing changed the cost story. |

## Takeaways

1. Scaling matters: moving a genuinely large `AGENTS.md` into dynamic skills produced clear token savings.
2. Progressive MCP discovery and scoped prompts produced large savings by reducing the context surface before work started.
3. Caveman-style terseness is best treated as an output-token technique; total observed tokens can still look worse when cache-read counters dominate a single run.
4. Multi-agent sharding can increase token volume while still lowering estimated cost if simpler subtasks run on cheaper models.
5. Compression should be measured with realistic history size; this fixture is intentionally capped for cross-platform CLI reliability.
