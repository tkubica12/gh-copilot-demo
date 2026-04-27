# Copilot token efficiency suite example

This is a sanitized example from a real local run with the Python runner, Copilot CLI backend, OpenTelemetry file export, and one measured iteration per variant. Treat the numbers as repeatable lab evidence, not universal pricing or billing data. Weighted units use the configurable rates in `model-pricing.toml`; GPT-5.5 and GPT-5.4 mini use the supplied Copilot price cards. For run-level details, see [reports/python-suite-2026-04-26.md](reports/python-suite-2026-04-26.md).

| Comparison | Technique idea | Baseline | Variant | Baseline input/output/cache | Variant input/output/cache | Raw-token result | Weighted-unit result | Output-token result | Other observations |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Always-on instructions | Move rarely needed details out of always-loaded instructions and reveal them as skills. | Large scaled multi-domain `AGENTS.md` | Small `AGENTS.md` plus one relevant skill | 154,908 / 280 / 0 | 42,749 / 550 / 27,648 | 54.3% saved | 68.8% saved | 96.4% more | Scaling unrelated always-on instructions made the skill-loading advantage visible. |
| MCP tool surface | Expose search/list tools first, then fetch only the selected resource. | 100 verbose direct MCP tools | Search-then-fetch MCP tools | 58,707 / 96 / 58,368 | 39,224 / 235 / 38,400 | 33.6% saved | 31.7% saved | 144.8% more | Progressive discovery still wins after output is weighted at 6x input because input/cache reductions dominate. |
| Prompt efficiency | Bound the input files and requested output shape instead of asking broadly. | Verbose open-ended prompt | Scoped files and five-bullet output contract | 139,922 / 2,062 / 114,688 | 38,563 / 235 / 37,376 | 70.3% saved | 73.3% saved | 88.6% saved | Tight file bounds and output shape reduced turns, tools, latency, and weighted units. |
| Compression simulation | Compare three resumed turns against fresh turns that carry only compact handoffs. | Three-turn accumulated session | Three fresh handoff sessions | 150,950 / 474 / 130,048 | 132,856 / 956 / 107,520 | 14.3% saved | 10.5% saved | 101.7% more | The handoff produces more output but lowers input/cache enough to keep weighted units lower. |
| Response style | Use a terse answer contract when polish and background are not needed. | Detailed incident guide | Caveman-inspired terse guide | 38,348 / 6,744 / 0 | 38,338 / 712 / 35,840 | 66.1% more | 41.4% saved | 89.4% saved | Weighting output exposes the real benefit: raw total worsened, but expensive output dropped sharply. |
| Workflow overhead | Split work only when orchestration overhead is worth the extra calls. | One small main-agent prompt | Three low-context mini-model shards | 38,312 / 400 / 17,408 | 114,156 / 400 / 71,680 | 231.9% more | 56.3% saved | 0.0% saved | Sharding small work used more raw tokens but GPT-5.4 mini pricing lowered weighted units. |
| Large-context sharding | Send focused subtasks to cheaper models while tracking repeated context cost. | One large accumulated-context prompt | Three focused mini-model shards | 38,933 / 611 / 37,376 | 127,976 / 635 / 110,592 | 211.0% more | 53.8% saved | 3.9% more | Separate mini-model calls still repeated context, but price-aware routing changed the cost story. |

## Takeaways

1. Scaling matters: moving a genuinely large `AGENTS.md` into dynamic skills produced clear token savings.
2. Progressive MCP discovery and scoped prompts produced large savings by reducing the context surface before work started.
3. Weighted units are the key metric when input, output, and cached tokens have different prices; raw totals are still useful diagnostics.
4. Caveman-style terseness is best treated as an output-token technique; total observed tokens can still look worse when cache-read counters dominate a single run.
5. Multi-agent sharding can increase token volume while still lowering estimated cost if simpler subtasks run on cheaper models.
6. Compression is now measured as a three-turn accumulated session versus fresh turns with compact handoffs, which is closer to how `/compact` changes the next working context.
