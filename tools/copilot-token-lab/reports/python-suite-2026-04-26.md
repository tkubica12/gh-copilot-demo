# Copilot token lab analysis

| Run | Group | Variant | Prompt | Technique | Model | Effort | Input | Output | Cache read | Cache create | Raw total | Weighted units | Estimated cost | Turns | Tools | Duration ms | Errors |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agents-big-gpt-5.5-medium-001-20260426214259 | agents-context | large-agents | agents-big | large-always-on-instructions | gpt-5.5 | medium | 154908 | 280 | 0 | 0 | 155188 | 782940 | 0.782940 | 1 | 0 | 9798.2 | 0 |
| agents-small-skill-gpt-5.5-medium-001-20260426214351 | agents-context | small-agents-skill | agents-small-skill | small-instructions-dynamic-skill | gpt-5.5 | medium | 42749 | 550 | 27648 | 0 | 70947 | 244069 | 0.244069 | 3 | 4 | 17056.1 | 0 |
| compression-full-history-gpt-5.5-medium-001-20260427080548 | compression-simulation | full-history | compression-full-history | uncompressed-history | gpt-5.5 | medium | 150950 | 474 | 130048 | 0 | 281472 | 833994 | 0.833994 | 3 | 0 | 5121.0 | 0 |
| compression-summary-gpt-5.5-medium-001-20260427080704 | compression-simulation | compressed-handoff | compression-summary | compressed-context | gpt-5.5 | medium | 132856 | 956 | 107520 | 0 | 241332 | 746720 | 0.746720 | 3 | 0 | 6339.2 | 0 |
| mcp-progressive-discovery-gpt-5.5-medium-001-20260426214556 | mcp-discovery | search-then-fetch | mcp-progressive-discovery | progressive-mcp-discovery | gpt-5.5 | medium | 39224 | 235 | 38400 | 0 | 77859 | 222370 | 0.222370 | 3 | 3 | 13659.3 | 0 |
| mcp-wide-tools-gpt-5.5-medium-001-20260426214502 | mcp-discovery | wide-100-tools | mcp-wide-tools | wide-tool-surface | gpt-5.5 | medium | 58707 | 96 | 58368 | 0 | 117171 | 325599 | 0.325599 | 2 | 1 | 10973.5 | 0 |
| prompt-efficient-gpt-5.5-medium-001-20260426220501 | prompt-efficiency | concise | prompt-efficient | scoped-output-contract | gpt-5.5 | medium | 38563 | 235 | 37376 | 0 | 76174 | 218553 | 0.218553 | 2 | 3 | 7037.3 | 0 |
| prompt-verbose-gpt-5.5-medium-001-20260426215609 | prompt-efficiency | verbose | prompt-verbose | over-specified-prompt | gpt-5.5 | medium | 139922 | 2062 | 114688 | 0 | 256672 | 818814 | 0.818814 | 5 | 14 | 30305.4 | 0 |
| response-caveman-gpt-5.5-medium-001-20260427063607 | response-style | caveman-terse | response-caveman | terse-output-contract | gpt-5.5 | medium | 38338 | 712 | 35840 | 0 | 74890 | 230970 | 0.230970 | 1 | 0 | 11683.9 | 0 |
| response-normal-gpt-5.5-medium-001-20260427063446 | response-style | normal | response-normal | normal-response-style | gpt-5.5 | medium | 38348 | 6744 | 0 | 0 | 45092 | 394060 | 0.394060 | 1 | 0 | 63561.9 | 0 |
| workflow-large-shard-backend-gpt-5.4-mini-low-001-20260426220326 | workflow-large-shards | focused-mini-shards | workflow-large-shard-backend | compressed-subtask-context | gpt-5.4-mini | low | 42714 | 249 | 36864 | 0 | 79827 | 35921 | 0.035921 | 2 | 2 | 6910.8 | 0 |
| workflow-large-shard-frontend-gpt-5.4-mini-low-001-20260426220309 | workflow-large-shards | focused-mini-shards | workflow-large-shard-frontend | compressed-subtask-context | gpt-5.4-mini | low | 42801 | 177 | 36864 | 0 | 79842 | 35662 | 0.035662 | 2 | 2 | 4228.1 | 0 |
| workflow-large-shard-ops-gpt-5.4-mini-low-001-20260426220345 | workflow-large-shards | focused-mini-shards | workflow-large-shard-ops | compressed-subtask-context | gpt-5.4-mini | low | 42461 | 209 | 36864 | 0 | 79534 | 35551 | 0.035551 | 2 | 2 | 5324.3 | 0 |
| workflow-large-single-gpt-5.5-medium-001-20260426220232 | workflow-large-shards | single-large-context | workflow-large-single | large-accumulated-context | gpt-5.5 | medium | 38933 | 611 | 37376 | 0 | 76920 | 231683 | 0.231683 | 4 | 11 | 24205.4 | 0 |
| workflow-shard-backend-gpt-5.4-mini-low-001-20260426214830 | workflow-overhead | orchestrated-mini-shards | workflow-shard-backend | external-low-context-subtask | gpt-5.4-mini | low | 38042 | 146 | 35840 | 0 | 74028 | 31876 | 0.031877 | 1 | 0 | 6556.3 | 0 |
| workflow-shard-frontend-gpt-5.4-mini-low-001-20260426214743 | workflow-overhead | orchestrated-mini-shards | workflow-shard-frontend | external-low-context-subtask | gpt-5.4-mini | low | 38068 | 120 | 0 | 0 | 38188 | 29091 | 0.029091 | 1 | 0 | 5473.1 | 0 |
| workflow-shard-ops-gpt-5.4-mini-low-001-20260426214917 | workflow-overhead | orchestrated-mini-shards | workflow-shard-ops | external-low-context-subtask | gpt-5.4-mini | low | 38046 | 134 | 35840 | 0 | 74020 | 31826 | 0.031825 | 1 | 0 | 6754.5 | 0 |
| workflow-single-agent-gpt-5.5-medium-001-20260426214653 | workflow-overhead | single-main-agent | workflow-single-agent | single-broad-context | gpt-5.5 | medium | 38312 | 400 | 17408 | 0 | 56120 | 212264 | 0.212264 | 1 | 0 | 8896.3 | 0 |

## Comparison groups

| Group | Variant | Weighted units | Weighted savings vs baseline | Raw tokens | Raw savings vs baseline | Input | Output | Output savings vs baseline | Cache read | Estimated cost | Cost savings vs baseline | Turns | Tools | Duration ms | Errors |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agents-context | large-agents | 782940 | 0.0% | 155188 | 0.0% | 154908 | 280 | 0.0% | 0 | 0.782940 | 0.0% | 1 | 0 | 9798.2 | 0 |
| agents-context | small-agents-skill | 244069 | 68.8% | 70947 | 54.3% | 42749 | 550 | -96.4% | 27648 | 0.244069 | 68.8% | 3 | 4 | 17056.1 | 0 |
| compression-simulation | full-history | 833994 | 0.0% | 281472 | 0.0% | 150950 | 474 | 0.0% | 130048 | 0.833994 | 0.0% | 3 | 0 | 5121.0 | 0 |
| compression-simulation | compressed-handoff | 746720 | 10.5% | 241332 | 14.3% | 132856 | 956 | -101.7% | 107520 | 0.746720 | 10.5% | 3 | 0 | 6339.2 | 0 |
| mcp-discovery | search-then-fetch | 222370 | 31.7% | 77859 | 33.6% | 39224 | 235 | -144.8% | 38400 | 0.222370 | 31.7% | 3 | 3 | 13659.3 | 0 |
| mcp-discovery | wide-100-tools | 325599 | 0.0% | 117171 | 0.0% | 58707 | 96 | 0.0% | 58368 | 0.325599 | 0.0% | 2 | 1 | 10973.5 | 0 |
| prompt-efficiency | concise | 218553 | 73.3% | 76174 | 70.3% | 38563 | 235 | 88.6% | 37376 | 0.218553 | 73.3% | 2 | 3 | 7037.3 | 0 |
| prompt-efficiency | verbose | 818814 | 0.0% | 256672 | 0.0% | 139922 | 2062 | 0.0% | 114688 | 0.818814 | 0.0% | 5 | 14 | 30305.4 | 0 |
| response-style | caveman-terse | 230970 | 41.4% | 74890 | -66.1% | 38338 | 712 | 89.4% | 35840 | 0.230970 | 41.4% | 1 | 0 | 11683.9 | 0 |
| response-style | normal | 394060 | 0.0% | 45092 | 0.0% | 38348 | 6744 | 0.0% | 0 | 0.394060 | 0.0% | 1 | 0 | 63561.9 | 0 |
| workflow-large-shards | focused-mini-shards | 107134 | 53.8% | 239203 | -211.0% | 127976 | 635 | -3.9% | 110592 | 0.107134 | 53.8% | 6 | 6 | 16463.2 | 0 |
| workflow-large-shards | single-large-context | 231683 | 0.0% | 76920 | 0.0% | 38933 | 611 | 0.0% | 37376 | 0.231683 | 0.0% | 4 | 11 | 24205.4 | 0 |
| workflow-overhead | orchestrated-mini-shards | 92793 | 56.3% | 186236 | -231.9% | 114156 | 400 | 0.0% | 71680 | 0.092793 | 56.3% | 3 | 0 | 18783.9 | 0 |
| workflow-overhead | single-main-agent | 212264 | 0.0% | 56120 | 0.0% | 38312 | 400 | 0.0% | 17408 | 0.212264 | 0.0% | 1 | 0 | 8896.3 | 0 |

## Interpretation checklist

1. Use weighted units or estimated cost as the headline comparison when pricing weights are available.
2. Treat lower tokens as a win only when task quality remains acceptable.
3. Inspect tool counts and errors before concluding a prompt is efficient.
4. Compare raw totals only between runs with the same Copilot client version and repository state.
5. Keep content capture disabled unless the environment is trusted.
