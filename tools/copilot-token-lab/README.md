# Copilot token lab

This side project measures GitHub Copilot token and latency behavior with a repeatable harness. It uses the documented GitHub Copilot CLI non-interactive mode plus OpenTelemetry file export, so it does not depend on private APIs or local session-store internals.

## What it proves

The lab compares the same repository task across different workflow techniques:

| Technique | What it tests |
| --- | --- |
| `baseline-broad-context` | Broad prompts that invite large context and long answers |
| `scoped-context-first` | Asking Copilot to identify the smallest useful file set before planning |
| `bounded-output` | Constraining answer shape and length |
| `summary-reuse` | Creating compact handoff summaries for later work |
| `small-instructions-dynamic-skill` | Replacing a large always-on `AGENTS.md` with short instructions plus an on-demand skill |
| `progressive-mcp-discovery` | Replacing a 100-tool MCP surface with search-then-fetch tools |
| `external-low-context-subtask` | Measuring cases where orchestration overhead can exceed the saved context |
| `compressed-subtask-context` | Testing whether focused mini-model shards beat one large accumulated context |
| `compressed-context` | Simulating `/compact` or handoff summaries after a context-heavy conversation |
| `scoped-output-contract` | Comparing verbose prompts with a tight input and output contract |

The included sample telemetry fixture demonstrates the expected pattern: the scoped prompt uses fewer observed tokens and fewer tools than the broad baseline. A real validation run with Copilot CLI 1.0.36 and `gpt-5.5` is captured in `example-analysis.md`; in that run, the scoped file-discovery prompt used about 72% fewer observed total tokens than the broad baseline. Real results depend on the selected model, Copilot client version, repository state, and network conditions.

## Prerequisites

- GitHub Copilot CLI on `PATH`
- Python 3.11+
- A trusted working directory
- Optional: a specific model selected with `-Model`; omit or use `auto` to let Copilot choose

## Run a dry run

Dry run creates the run folder structure without calling a model:

```powershell
.\tools\copilot-token-lab\Invoke-CopilotTokenLab.ps1 -Iterations 1
```

## Run real measurements

This executes prompts with Copilot CLI and writes one OTel JSONL file per run:

```powershell
.\tools\copilot-token-lab\Invoke-CopilotTokenLab.ps1 `
  -Execute `
  -Iterations 3 `
  -Model auto `
  -OutputDir .\tools\copilot-token-lab\runs
```

For prompts that may need shell/file tools, add `-AllowAllTools` only in a trusted repo and preferably with read-only prompts first.

## Run the full efficiency suite

The suite creates isolated fixture workspaces and a generated prompt catalog, then runs the same harness:

```powershell
.\tools\copilot-token-lab\Invoke-TokenEfficiencySuite.ps1 `
  -Execute `
  -AllowAllTools `
  -Iterations 1 `
  -OutputDir .\tools\copilot-token-lab\suite-runs
```

It covers these comparison groups:

| Group | Variants |
| --- | --- |
| `agents-context` | large always-on `AGENTS.md` versus small `AGENTS.md` plus `.github\skills\addon-routing` |
| `mcp-discovery` | MCP server with 100 direct action tools versus search-then-fetch discovery tools |
| `workflow-overhead` | one small main-agent prompt versus externally orchestrated mini-model shards |
| `workflow-large-shards` | one large accumulated-context prompt versus focused mini-model shards |
| `compression-simulation` | uncompressed simulated turn history versus compressed handoff summary |
| `prompt-efficiency` | verbose prompt versus concise prompt with explicit file and output bounds |

Use a dry run first by omitting `-Execute`. The generated MCP servers are local stdio servers in `mcp_servers\token_lab_mcp.py`.

## Analyze runs

```powershell
python .\tools\copilot-token-lab\analyze_otel.py `
  --runs .\tools\copilot-token-lab\runs `
  --output .\tools\copilot-token-lab\runs\analysis.md
```

The report includes input, output, cache-read, cache-creation, total observed tokens, turn count, tool count, duration, and errors. When prompts include `comparisonGroup` and `variant`, it also writes grouped savings versus the first variant in each group.

For checked-in examples, see `example-analysis.md` for the original broad-versus-scoped run and `suite-example-analysis.md` for the expanded benchmark matrix.

## Test the analyzer

```powershell
python -m unittest discover -s .\tools\copilot-token-lab\tests
```

The tests use checked-in sample OTel JSONL fixtures. They validate that the analyzer can detect token differences between broad and scoped prompt styles before you spend real Copilot usage.

## Measurement protocol

1. Keep the repository state fixed.
2. Disable demo hooks unless measuring hook overhead.
3. Run 3-5 warmups and 10-30 measured runs for serious comparisons.
4. Compare medians and p90/p95, not single runs.
5. Treat token reduction as a win only when task quality remains acceptable.
6. Keep full content capture disabled unless the environment is trusted.

## Important limitations

- OTel token counts are usage telemetry, not a guaranteed invoice replica.
- Copilot and model behavior are nondeterministic; repeat runs are required.
- New Copilot versions may add fields; the analyzer is intentionally tolerant but should be reviewed when clients change.
- Do not reverse-engineer private endpoints or parse undocumented session internals for billing data.
