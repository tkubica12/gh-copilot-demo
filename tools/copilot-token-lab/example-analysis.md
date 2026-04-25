# Copilot token lab example analysis

This is a sanitized example from a real local run using GitHub Copilot CLI 1.0.36, `-p` non-interactive mode, `COPILOT_OTEL_FILE_EXPORTER_PATH`, and model `gpt-5.5`. Treat it as evidence that the harness works end-to-end, not as a universal benchmark.

| Prompt | Technique | Model | Input | Output | Cache read | Total observed tokens | Turns | Tools | Duration ms | Errors |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `broad-repo-summary` | `baseline-broad-context` | `gpt-5.5` | 1,531,835 | 10,702 | 1,431,552 | 2,974,089 | 16 | 93 | 99,269.8 | 5 |
| `scoped-file-discovery` | `scoped-context-first` | `gpt-5.5` | 441,349 | 3,074 | 378,880 | 823,303 | 10 | 30 | 157,344.1 | 0 |

## Observed outcome

The scoped prompt used **2,150,786 fewer observed tokens** than the broad prompt, a reduction of about **72.3%** in this run. It also used fewer turns and tools. The scoped run took longer wall-clock time, which is why the lab tracks both tokens and latency instead of optimizing one metric in isolation.

## Interpretation

Use this as a workshop talking point:

1. Token-efficient context can materially reduce model work.
2. The agent may still choose broad tools if the prompt is not explicit enough; inspect tool count and errors.
3. Token savings must be balanced with outcome quality and latency.
4. Repeat runs before making policy or model-selection decisions.
