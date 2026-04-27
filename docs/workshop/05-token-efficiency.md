[Workshop index](README.md) | [Repository README](../../README.md)

---

# 5. Save tokens with context hygiene

This chapter turns token efficiency into a measurable engineering practice. It summarizes the lecture guidance and links to the repeatable Copilot CLI measurement lab.

## Measured benchmark summary

These results come from a real local run of the reusable suite in `..\..\tools\copilot-token-lab`. Treat them as lab evidence and rerun the suite for current client, model, and repository state.

| Test | Baseline | Token-efficient variant | Total-token result | Output-token result | Cost-unit result |
| --- | --- | --- | ---: | ---: | ---: |
| AGENTS.md vs skills | Large scaled multi-domain `AGENTS.md` | Small `AGENTS.md` plus one relevant skill | 54.3% saved | 96.4% more | 69.4% saved |
| Progressive MCP discovery | 100 verbose direct MCP tools | Search-then-fetch MCP tools | 33.6% saved | 144.8% more | 32.2% saved |
| Prompt efficiency | Verbose open-ended prompt | Scoped files plus output contract | 70.3% saved | 88.6% saved | 72.9% saved |
| Compression simulation | Three-turn accumulated session | Three fresh handoff sessions | 14.3% saved | 101.7% more | 11.1% saved |
| Caveman-style response | Detailed incident guide | Terse output contract | 66.1% more | 89.4% saved | 31.5% saved |
| Multi-agent overhead case | One small main-agent prompt | Three mini-model shard calls | 231.9% more | 0.0% saved | 26.2% saved |
| Large-context sharding attempt | One large accumulated-context prompt | Three focused mini-model shards | 211.0% more | 3.9% more | 21.5% saved |

Details: [suite example analysis](../../tools/copilot-token-lab/suite-example-analysis.md), [full Python run report](../../tools/copilot-token-lab/reports/python-suite-2026-04-26.md), [rerun instructions](../../tools/copilot-token-lab/README.md), and [generated scenario fixtures](../../tools/copilot-token-lab/scenario_builder.py). Cost units are relative demo estimates from `model-pricing.toml`, not official prices. Output-token savings are shown separately because terse response styles optimize answer length, not always-on context.

Token efficiency is not about starving Copilot of context. It is about giving Copilot the smallest high-signal working set that lets it solve the task correctly.

### Concepts to explain first

Tokens are consumed by more than the words you type. They can come from:

- always-on instructions such as `AGENTS.md` and repository custom instructions
- selected files, open editor context, images, logs, and tool results
- chat history and summaries carried between turns
- model output
- additional model calls triggered by agents, tools, retries, and subagents

The practical goal is **scoped sufficiency**: enough context to be precise, no more than needed. Too little context can produce vague answers and repeated retries; too much context slows the task, makes answers harder to review, and can waste tokens.

### Token-efficient patterns

| Expensive pattern | Token-efficient version |
| --- | --- |
| Paste the whole README, specs, and logs | Ask which files or excerpts matter first |
| Keep every rule in always-on instructions | Put stable rules in `AGENTS.md`; put detailed workflows in prompt files or skills |
| Ask MCP to fetch everything | Search or list first, then fetch one selected result |
| Use `/fleet` for every problem | Use subagents only when work is genuinely parallel |
| Send terminal screenshots | Paste exact text excerpts unless visual layout matters |
| Stay in a stale long session forever | Use `/context`, `/compact`, `/research`, or start fresh |
| Request a polished essay when terse output is enough | Use a Caveman-style response contract: short, direct, no pleasantries |

### Use durable context instead of repeated explanations

This repository already has reusable context assets:

- `AGENTS.md` for stable engineering rules
- `PRD.md` for product intent
- `specs\` for architecture, security, testing, deployment, and runbooks
- `.github\prompts\` for reusable workflow starts
- `.github\skills\` for detailed local capabilities that load only when relevant

Use those assets as references instead of re-explaining the same background in every prompt. Keep `AGENTS.md` compact because it is part of the recurring context tax; move verbose, task-specific procedures into prompt files, skills, or docs that Copilot can retrieve only when needed.

### Prefer skills and MCP as progressive reveal

Skills and MCP are token-saving mechanisms when used carefully:

- **Skills** load detailed instructions, scripts, and examples only when the task matches the skill description.
- **MCP tools** should retrieve targeted live data instead of forcing you to paste large docs, issue lists, or logs.

Good MCP workflow:

1. Search or list candidate resources.
2. Pick the relevant resource.
3. Fetch only the details needed for the current decision.
4. Summarize the result before continuing.

Avoid MCP tools that return unlimited logs or entire workspaces by default. Prefer summary, paging, limits, and exact excerpts.

### Use agents and subagents economically

Subagents are context-isolation tools, not automatic token savers. The best mental model is the context-engineering loop described by Anthropic and LangChain: **write, select, compress, and isolate** context. Subagents help with the "isolate" part because each worker gets its own context window, tools, and instructions, but isolation can multiply tokens if each worker reloads the same files or receives the same long briefing.

In this repo:

- `researcher` is read-only and returns short, high-signal file summaries.
- `implementer` makes small, isolated edits after the research is done.
- `task` is useful for tests and builds because successful output stays short while failures keep the useful details.

Use this decision table before delegating:

| Question | Token implication | Better default |
| --- | --- | --- |
| Can the subtask run independently? | Independent shards can run with narrow context; dependent shards need repeated coordination. | Delegate independent research, test, or file-inspection tasks. |
| What must the main agent pass? | The handoff is main-agent **output tokens**, often from an expensive model. | Pass objective, constraints, exact files, and output schema; avoid long narrative history. |
| Will the subagent reread files the main agent already loaded? | Main-thread history may be cached on later turns, while subagent file reads are new input tokens. | Use subagents when cheaper model input or isolation outweighs duplicated reads. |
| Will parallel agents inspect overlapping context? | Parallelism can multiply input tokens by N if workers load the same repo slices. | Split by non-overlapping files, services, or questions. |
| Is the long thread still useful? | Long sessions preserve nuance, but cost, latency, and context confusion grow. | Keep long threads while coherence matters; compact or restart when stale context dominates. |
| Can durable notes replace history? | High-density files or scratchpads let future sessions reload compressed state on demand. | Ask agents to write short handoff files with decisions, file paths, constraints, and validation. |

The economic tradeoff is a ratio:

```text
subagent value ≈ saved main-agent context + cheaper subagent model
                 - handoff output tokens
                 - duplicated subagent input/tool tokens
                 - coordination/retry overhead
```

Caching complicates the model. If the main agent already paid to load a large file set, the next turn may reuse cached input pricing, while a subagent reading the same files usually pays fresh input. That can make a long main-agent thread cheaper than delegation even when the subagent model is smaller. Conversely, if the main thread is bloated with stale logs and tool results, a fresh subagent plus a dense handoff can improve both cost and quality.

Do not use subagents reflexively. Anthropic's production research system reports that multi-agent systems can substantially improve broad research quality, but also that multi-agent systems burn tokens quickly and fit best when the task is valuable, parallelizable, and larger than one context window. Coding work is often less parallel than research, so delegate with explicit effort budgets and evaluate both outcome quality and token/cost telemetry.

Practical patterns:

1. **Handoff small**: objective, known facts, exact files, constraints, acceptance criteria, output format.
2. **Shard by ownership**: one worker per service, file family, or question; avoid overlapping scans.
3. **Use cheap models intentionally**: route extraction, summarization, and test-output triage to mini models; keep architecture and hard debugging on stronger models.
4. **Write high-density state**: use `HANDOFF.md`, scratch notes, or implementation logs so new sessions can select compressed context instead of replaying the chat.
5. **Compact before quality drops**: use `/compact` or a manual handoff when context is mostly stale tool output, but keep the long thread when nuanced decisions are still actively shaping work.

Further reading: [Anthropic on multi-agent research](https://www.anthropic.com/engineering/built-multi-agent-research-system), [Anthropic on context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [LangChain on write/select/compress/isolate](https://blog.langchain.com/context-engineering-for-agents/), and [Google ADK on scoped multi-agent context](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/).

### Choose the right model

Default to **Auto** when unsure, then override intentionally:

| Task | Model strategy |
| --- | --- |
| Formatting, extraction, simple docs | Auto or a smaller/faster model |
| File discovery and repo orientation | Fast exploration or read-only subagent |
| Test/build execution | Deterministic shell or `task` agent |
| Architecture decisions and hard debugging | Stronger model or higher reasoning effort |
| Multi-file implementation | Stronger model with scoped files and a plan |

Price per token is not the whole story. A stronger or newer model can be more efficient if it solves the task in fewer turns with fewer retries. Treat model efficiency as something to measure on your workload, not as a universal rule.

### Text, screenshots, and logs

Use text for text. Paste exact error messages, stack traces, JSON, YAML, shell output, or code whenever possible. Use screenshots when visual layout matters, such as UI alignment or rendered diagrams, and crop them aggressively.

For logs, start with:

1. one-sentence problem summary
2. exact command or CI job
3. first error, final error, and 20-50 surrounding lines
4. environment and recent change
5. full log only if needed

This gives Copilot the failure signal without burying it in thousands of irrelevant lines.

### Measure instead of guessing

OpenTelemetry turns token hygiene from advice into evidence. The side project in `tools\copilot-token-lab` provides a repeatable Python harness with TOML configuration. Its default backend invokes Copilot CLI because that is the validated interface for exporting token telemetry today:

```shell
cd tools/copilot-token-lab
uv run python run_token_lab.py suite --execute --allow-all-tools --iterations 3 --output-dir suite-runs
uv run python run_token_lab.py analyze --runs suite-runs/runs --output suite-runs/analysis.md
```

The harness uses Copilot CLI non-interactive mode and `COPILOT_OTEL_FILE_EXPORTER_PATH` to write one telemetry file per run. Compare input tokens, output tokens, cached input tokens, turn count, tool count, duration, errors, relative cost units, and task quality across broad prompts, scoped prompts, summaries, response styles, and model choices. The runner has a backend boundary for a future SDK implementation, but the SDK path should only be enabled when it exposes equivalent telemetry.

### Try this

Start with a file-discovery prompt:

```text
Find the smallest set of files I should give Copilot to understand the event-driven add-on flow. Do not summarize the whole repo; return only file paths and why each matters.
```

Then constrain the output:

```text
Using only those files, create a concise implementation plan. Keep the output under 20 lines and include validation steps.
```

Then create a reusable handoff:

```text
Compact this session into a handoff summary for implementation. Keep only decisions, relevant files, constraints, and validation steps.
```

### What to observe

- smaller context can produce better answers when the context is higher signal
- skills and MCP are progressive-reveal tools, not excuses to dump more data into chat
- subagents can reduce main-thread clutter, but parallel agents multiply work
- Auto model selection is a good default, but model choice should match task complexity
- OpenTelemetry makes token usage, model choice, tool calls, and latency visible enough to compare techniques


---

Previous: [Copilot CLI](04-copilot-cli.md) | Next: [Governance, review, security, and hooks](06-governance-review-security-hooks.md)
