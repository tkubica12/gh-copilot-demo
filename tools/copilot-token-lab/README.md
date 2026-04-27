# Copilot token lab

This side project measures GitHub Copilot token and latency behavior with a repeatable, cross-platform Python harness. The default backend uses documented GitHub Copilot CLI non-interactive mode plus OpenTelemetry file export, so it does not depend on private APIs or local session-store internals.

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
| `terse-output-contract` | Testing Caveman-inspired terse responses that reduce output tokens |

The included sample telemetry fixture demonstrates the expected pattern: the scoped prompt uses fewer observed tokens and fewer tools than the broad baseline. A real validation run with Copilot CLI 1.0.36 and `gpt-5.5` is captured in `example-analysis.md`; in that run, the scoped file-discovery prompt used about 72% fewer observed total tokens than the broad baseline. Real results depend on the selected model, Copilot client version, repository state, and network conditions.

## Prerequisites

- GitHub Copilot CLI on `PATH`
- Python 3.11+
- Optional but recommended: `uv`
- A trusted working directory
- Optional: edit `token-lab.toml` to change backend, output folders, iteration count, default model/effort lists, and the relative pricing file

## Why the backend is still Copilot CLI

The harness is now Python and TOML based, but it still invokes Copilot CLI by default because the lab needs token telemetry, tool counts, model metadata, and run artifacts. Copilot CLI with `COPILOT_OTEL_FILE_EXPORTER_PATH` is the validated interface that provides those signals today. `run_token_lab.py` has a backend boundary and an explicit `sdk` placeholder; add an SDK backend there when a stable GitHub Copilot SDK exposes equivalent telemetry.

## Run a dry run

Dry run creates the run folder structure without calling a model:

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py suite --dry-run --output-dir suite-runs-dry
```

## Run real measurements

This executes prompts with Copilot CLI and writes one OTel JSONL file per run:

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py suite --execute --allow-all-tools --iterations 3 --output-dir suite-runs
```

For prompts that may need shell/file tools, add `--allow-all-tools` only in a trusted repo and preferably with read-only prompts first.

## Run the full efficiency suite

The suite creates isolated fixture workspaces and a generated prompt catalog, then runs the same harness:

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py suite --execute --allow-all-tools --iterations 1 --output-dir suite-runs
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
| `response-style` | normal explanatory response versus a Caveman-inspired terse output contract |

Use a dry run first by omitting `--execute`. The generated MCP servers are local stdio servers in `mcp_servers\token_lab_mcp.py`.

## Analyze runs

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py analyze --runs suite-runs/runs --output suite-runs/analysis.md --pricing model-pricing.toml
```

The report includes input, output, cache-read, cache-creation, total observed tokens, relative cost units, turn count, tool count, duration, and errors. When prompts include `comparisonGroup` and `variant`, it also writes grouped total-token, output-token, and cost savings versus the baseline variant. `model-pricing.toml` contains replaceable demo rates, not official GitHub pricing.

For checked-in examples, see `example-analysis.md` for the original broad-versus-scoped run, `suite-example-analysis.md` for the expanded benchmark matrix, and `reports/python-suite-2026-04-26.md` for a run-level Python suite report.

## Test the analyzer

```shell
cd tools/copilot-token-lab
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

The tests are split by concern:

- `tests/test_analyzer.py` validates OTel parsing and report generation.
- `tests/test_scenario_builder.py` validates generated benchmark families.
- `tests/test_runner.py` validates TOML configuration and dry-run output.

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
