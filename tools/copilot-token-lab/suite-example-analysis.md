# Copilot token efficiency suite example

This is a sanitized example from a real local run with the Python runner, Copilot CLI backend, OpenTelemetry file export, and one measured iteration per variant. Treat the numbers as repeatable lab evidence, not universal pricing or billing data. Weighted units use the configurable rates in `model-pricing.toml`; GPT-5.5 and GPT-5.4 mini use the supplied Copilot price cards. For run-level details, see [reports/python-suite-2026-04-26.md](reports/python-suite-2026-04-26.md).

| Comparison | Technique idea | Baseline | Variant | Weighted result | Note |
| --- | --- | --- | --- | ---: | --- |
| Always-on instructions | Move rarely needed details out of always-loaded instructions and reveal them as skills. | Large scaled multi-domain `AGENTS.md`<br>in 154,908 / cache 0 / out 280 / weighted 782,940 | Small `AGENTS.md` plus one relevant skill<br>in 42,749 / cache 27,648 / out 550 / weighted 244,069 | 68.8% saved | Raw tokens also fell 54.3%; the variant produced more output but removed enough always-on input to win. |
| MCP tool surface | Expose search/list tools first, then fetch only the selected resource. | 100 verbose direct MCP tools<br>in 58,707 / cache 58,368 / out 96 / weighted 325,599 | Search-then-fetch MCP tools<br>in 39,224 / cache 38,400 / out 235 / weighted 222,370 | 31.7% saved | Progressive discovery still wins after output is weighted because input/cache reductions dominate. |
| Prompt efficiency | Bound the input files and requested output shape instead of asking broadly. | Verbose open-ended prompt<br>in 139,922 / cache 114,688 / out 2,062 / weighted 818,814 | Scoped files and five-bullet output contract<br>in 38,563 / cache 37,376 / out 235 / weighted 218,553 | 73.3% saved | Tight file bounds and output shape reduced turns, tools, latency, and weighted units. |
| Compression simulation | Compare three resumed turns against fresh turns that carry only compact handoffs. | Three-turn accumulated session<br>in 150,950 / cache 130,048 / out 474 / weighted 833,994 | Three fresh handoff sessions<br>in 132,856 / cache 107,520 / out 956 / weighted 746,720 | 10.5% saved | The handoff produces more output but lowers input/cache enough to keep weighted units lower. |
| Response style | Use a terse answer contract when polish and background are not needed. | Detailed incident guide<br>in 38,348 / cache 0 / out 6,744 / weighted 394,060 | Caveman-inspired terse guide<br>in 38,338 / cache 35,840 / out 712 / weighted 230,970 | 41.4% saved | Raw total worsened, but expensive output dropped from 6,744 to 712 tokens. |
| Workflow overhead | Split work only when orchestration overhead is worth the extra calls. | One small main-agent prompt<br>in 38,312 / cache 17,408 / out 400 / weighted 212,264 | Three low-context mini-model shards<br>in 114,156 / cache 71,680 / out 400 / weighted 92,793 | 56.3% saved | Raw tokens increased 231.9%, but GPT-5.4 mini pricing lowered weighted units. |
| Large-context sharding | Send focused subtasks to cheaper models while tracking repeated context cost. | One large accumulated-context prompt<br>in 38,933 / cache 37,376 / out 611 / weighted 231,683 | Three focused mini-model shards<br>in 127,976 / cache 110,592 / out 635 / weighted 107,134 | 53.8% saved | Separate mini-model calls still repeated context, but price-aware routing changed the cost story. |

## Takeaways

1. Scaling matters: moving a genuinely large `AGENTS.md` into dynamic skills produced clear token savings.
2. Progressive MCP discovery and scoped prompts produced large savings by reducing the context surface before work started.
3. Weighted units are the key metric when input, output, and cached tokens have different prices; inspect raw totals in the full report when you need diagnostics.
4. Caveman-style terseness is best treated as an output-token technique; raw observed tokens can still look worse when cache-read counters dominate a single run.
5. Multi-agent sharding can increase token volume while still lowering estimated cost if simpler subtasks run on cheaper models.
6. Compression is now measured as a three-turn accumulated session versus fresh turns with compact handoffs, which is closer to how `/compact` changes the next working context.
