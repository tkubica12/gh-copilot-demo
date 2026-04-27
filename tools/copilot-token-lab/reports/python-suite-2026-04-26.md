# Copilot token lab analysis

| Run | Group | Variant | Prompt | Technique | Model | Effort | Input | Output | Cache read | Cache create | Total | Cost units | Turns | Tools | Duration ms | Errors |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agents-big-gpt-5.5-medium-001-20260426214259 | agents-context | large-agents | agents-big | large-always-on-instructions | gpt-5.5 | medium | 154908 | 280 | 0 | 0 | 155188 | 0.156028 | 1 | 0 | 9798.2 | 0 |
| agents-small-skill-gpt-5.5-medium-001-20260426214351 | agents-context | small-agents-skill | agents-small-skill | small-instructions-dynamic-skill | gpt-5.5 | medium | 42749 | 550 | 27648 | 0 | 70947 | 0.047714 | 3 | 4 | 17056.1 | 0 |
| compression-full-history-gpt-5.5-medium-001-20260427080548 | compression-simulation | full-history | compression-full-history | uncompressed-history | gpt-5.5 | medium | 150950 | 474 | 130048 | 0 | 281472 | 0.165851 | 3 | 0 | 5121.0 | 0 |
| compression-summary-gpt-5.5-medium-001-20260427080704 | compression-simulation | compressed-handoff | compression-summary | compressed-context | gpt-5.5 | medium | 132856 | 956 | 107520 | 0 | 241332 | 0.147432 | 3 | 0 | 6339.2 | 0 |
| mcp-progressive-discovery-gpt-5.5-medium-001-20260426214556 | mcp-discovery | search-then-fetch | mcp-progressive-discovery | progressive-mcp-discovery | gpt-5.5 | medium | 39224 | 235 | 38400 | 0 | 77859 | 0.044004 | 3 | 3 | 13659.3 | 0 |
| mcp-wide-tools-gpt-5.5-medium-001-20260426214502 | mcp-discovery | wide-100-tools | mcp-wide-tools | wide-tool-surface | gpt-5.5 | medium | 58707 | 96 | 58368 | 0 | 117171 | 0.064928 | 2 | 1 | 10973.5 | 0 |
| prompt-efficient-gpt-5.5-medium-001-20260426220501 | prompt-efficiency | concise | prompt-efficient | scoped-output-contract | gpt-5.5 | medium | 38563 | 235 | 37376 | 0 | 76174 | 0.043241 | 2 | 3 | 7037.3 | 0 |
| prompt-verbose-gpt-5.5-medium-001-20260426215609 | prompt-efficiency | verbose | prompt-verbose | over-specified-prompt | gpt-5.5 | medium | 139922 | 2062 | 114688 | 0 | 256672 | 0.159639 | 5 | 14 | 30305.4 | 0 |
| response-caveman-gpt-5.5-medium-001-20260427063607 | response-style | caveman-terse | response-caveman | terse-output-contract | gpt-5.5 | medium | 38338 | 712 | 35840 | 0 | 74890 | 0.044770 | 1 | 0 | 11683.9 | 0 |
| response-normal-gpt-5.5-medium-001-20260427063446 | response-style | normal | response-normal | normal-response-style | gpt-5.5 | medium | 38348 | 6744 | 0 | 0 | 45092 | 0.065324 | 1 | 0 | 63561.9 | 0 |
| workflow-large-shard-backend-gpt-5.4-mini-low-001-20260426220326 | workflow-large-shards | focused-mini-shards | workflow-large-shard-backend | compressed-subtask-context | gpt-5.4-mini | low | 42714 | 249 | 36864 | 0 | 79827 | 0.011849 | 2 | 2 | 6910.8 | 0 |
| workflow-large-shard-frontend-gpt-5.4-mini-low-001-20260426220309 | workflow-large-shards | focused-mini-shards | workflow-large-shard-frontend | compressed-subtask-context | gpt-5.4-mini | low | 42801 | 177 | 36864 | 0 | 79842 | 0.011799 | 2 | 2 | 4228.1 | 0 |
| workflow-large-shard-ops-gpt-5.4-mini-low-001-20260426220345 | workflow-large-shards | focused-mini-shards | workflow-large-shard-ops | compressed-subtask-context | gpt-5.4-mini | low | 42461 | 209 | 36864 | 0 | 79534 | 0.011746 | 2 | 2 | 5324.3 | 0 |
| workflow-large-single-gpt-5.5-medium-001-20260426220232 | workflow-large-shards | single-large-context | workflow-large-single | large-accumulated-context | gpt-5.5 | medium | 38933 | 611 | 37376 | 0 | 76920 | 0.045115 | 4 | 11 | 24205.4 | 0 |
| workflow-shard-backend-gpt-5.4-mini-low-001-20260426214830 | workflow-overhead | orchestrated-mini-shards | workflow-shard-backend | external-low-context-subtask | gpt-5.4-mini | low | 38042 | 146 | 35840 | 0 | 74028 | 0.010552 | 1 | 0 | 6556.3 | 0 |
| workflow-shard-frontend-gpt-5.4-mini-low-001-20260426214743 | workflow-overhead | orchestrated-mini-shards | workflow-shard-frontend | external-low-context-subtask | gpt-5.4-mini | low | 38068 | 120 | 0 | 0 | 38188 | 0.009637 | 1 | 0 | 5473.1 | 0 |
| workflow-shard-ops-gpt-5.4-mini-low-001-20260426214917 | workflow-overhead | orchestrated-mini-shards | workflow-shard-ops | external-low-context-subtask | gpt-5.4-mini | low | 38046 | 134 | 35840 | 0 | 74020 | 0.010542 | 1 | 0 | 6754.5 | 0 |
| workflow-single-agent-gpt-5.5-medium-001-20260426214653 | workflow-overhead | single-main-agent | workflow-single-agent | single-broad-context | gpt-5.5 | medium | 38312 | 400 | 17408 | 0 | 56120 | 0.041653 | 1 | 0 | 8896.3 | 0 |

## Comparison groups

| Group | Variant | Total observed tokens | Savings vs baseline | Output tokens | Output savings vs baseline | Cost units | Cost savings vs baseline | Turns | Tools | Duration ms | Errors |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agents-context | large-agents | 155188 | 0.0% | 280 | 0.0% | 0.156028 | 0.0% | 1 | 0 | 9798.2 | 0 |
| agents-context | small-agents-skill | 70947 | 54.3% | 550 | -96.4% | 0.047714 | 69.4% | 3 | 4 | 17056.1 | 0 |
| compression-simulation | full-history | 281472 | 0.0% | 474 | 0.0% | 0.165851 | 0.0% | 3 | 0 | 5121.0 | 0 |
| compression-simulation | compressed-handoff | 241332 | 14.3% | 956 | -101.7% | 0.147432 | 11.1% | 3 | 0 | 6339.2 | 0 |
| mcp-discovery | search-then-fetch | 77859 | 33.6% | 235 | -144.8% | 0.044004 | 32.2% | 3 | 3 | 13659.3 | 0 |
| mcp-discovery | wide-100-tools | 117171 | 0.0% | 96 | 0.0% | 0.064928 | 0.0% | 2 | 1 | 10973.5 | 0 |
| prompt-efficiency | concise | 76174 | 70.3% | 235 | 88.6% | 0.043241 | 72.9% | 2 | 3 | 7037.3 | 0 |
| prompt-efficiency | verbose | 256672 | 0.0% | 2062 | 0.0% | 0.159639 | 0.0% | 5 | 14 | 30305.4 | 0 |
| response-style | caveman-terse | 74890 | -66.1% | 712 | 89.4% | 0.044770 | 31.5% | 1 | 0 | 11683.9 | 0 |
| response-style | normal | 45092 | 0.0% | 6744 | 0.0% | 0.065324 | 0.0% | 1 | 0 | 63561.9 | 0 |
| workflow-large-shards | focused-mini-shards | 239203 | -211.0% | 635 | -3.9% | 0.035394 | 21.5% | 6 | 6 | 16463.2 | 0 |
| workflow-large-shards | single-large-context | 76920 | 0.0% | 611 | 0.0% | 0.045115 | 0.0% | 4 | 11 | 24205.4 | 0 |
| workflow-overhead | orchestrated-mini-shards | 186236 | -231.9% | 400 | 0.0% | 0.030731 | 26.2% | 3 | 0 | 18783.9 | 0 |
| workflow-overhead | single-main-agent | 56120 | 0.0% | 400 | 0.0% | 0.041653 | 0.0% | 1 | 0 | 8896.3 | 0 |

## Interpretation checklist

1. Compare total tokens only between runs with the same Copilot client version and repository state.
2. Treat lower tokens as a win only when task quality remains acceptable.
3. Inspect tool counts and errors before concluding a prompt is efficient.
4. Cost units are relative estimates when model-pricing.toml is supplied.
5. Keep content capture disabled unless the environment is trusted.
