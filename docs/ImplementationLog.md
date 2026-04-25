# Implementation Log

## 2026-04-25 – Split workshop guide into chapter files

Moved the long workshop lecture out of the root `README.md` and into focused chapter files under `docs\workshop`.

### Decisions
- Kept the existing course flow but promoted token efficiency into its own chapter after Copilot CLI execution.
- Converted the root `README.md` into a concise landing page with links to the detailed chapters.
- Added the measured token-efficiency benchmark table to `docs\workshop\05-token-efficiency.md` with links to the reusable lab details.

## 2026-04-25 – Added token-efficiency workshop chapter and measurement lab

Added a late Chapter 5 section that teaches Copilot token efficiency as context hygiene, workflow design, model choice, and measurement rather than just shorter prompts.

### Decisions
- Inserted the token-efficiency material after execution surfaces so the workshop first introduces CLI sessions, agents, skills, MCP, and model selection before discussing how to use them economically.
- Added `tools\copilot-token-lab` as a repeatable Copilot CLI plus OpenTelemetry harness with prompt catalog, PowerShell runner, analyzer, sample telemetry, and unit tests.
- Expanded the lab with generated benchmark fixtures for large versus small instructions, wide versus progressive MCP discovery, single-agent versus decomposed workflow shape, compression, and verbose versus scoped prompting.
- Revised the benchmark matrix to remove model-comparison claims, make AGENTS-versus-skills compare unrelated always-on context against one relevant skill, and add compression simulation for compacted handoffs.
- Kept the measurement path on documented surfaces: Copilot CLI `-p` and `COPILOT_OTEL_FILE_EXPORTER_PATH`; avoided private APIs and undocumented session-store parsing.
- Documented screenshots/logs/model-choice guidance as measurement hypotheses where official billing or model-efficiency data is not directly available.

## 2026-03-24 – Added live custom-agent creation to the workshop flow

Expanded the custom-agents chapter so the workshop now demonstrates creating a new specialist with `/create-agent`, not only using the prebuilt agents already stored in the repository.

### Decisions
- Added a concrete `/create-agent` exercise to the main `README.md` custom-agents chapter using a business-analytics-to-PRD example.
- Positioned the exercise after handoffs so the audience first understands prebuilt agents and then sees live agent creation from natural language.
- Updated `docs/enterprise_demo_flow.md` so the condensed presenter notes reinforce the same custom-agent creation step.

## 2026-03-19 – Removed dormant-mode hook gating and simplified activation

Simplified the hook demo so the generated repository policy file is the only activation mechanism. There is no longer a separate flag file or environment-variable override inside the hook scripts.

### Decisions
- Removed the `demo-enabled.flag` and `COPILOT_DEMO_HOOKS` checks from the PowerShell and bash hook helpers so installed hooks always execute.
- Removed the temporary install/remove helper scripts as unnecessary ceremony and documented the manual `Copy-Item` / `Remove-Item` workflow instead.
- Ignored generated `.github\hooks\copilot-policy.json` in `.gitignore` so workshop activation does not dirty the repository.
- Updated the workshop docs to describe install/remove semantics instead of dormant-mode toggling.

## 2026-03-19 – Made workshop hooks truly opt-in for VS Code and CLI sessions

Adjusted the hook demo so disabling it removes the active repository hook policy instead of only short-circuiting inside the scripts. This prevents Copilot clients from invoking hook processes at all when the workshop demo is not enabled.

### Decisions
- Replaced the checked-in runtime hook policy with a template file and now materialize `.github\hooks\copilot-policy.json` only when the hook demo is installed for the workshop chapter.
- Removed the active runtime policy file when the hook demo is no longer installed so "disabled" means no hooks are registered.
- Updated the workshop documentation to explain the generated policy file and to advise starting a fresh Copilot session after toggling hooks, which is safer for VS Code preview behavior.

## 2026-03-18 – Made workshop hooks opt-in and safer for live demos

Adjusted the repository hook demo so it no longer interferes with normal Copilot CLI usage outside the hooks chapter.

### Decisions
- Changed the hook scripts to stay dormant unless the local demo toggle is explicitly enabled.
- Fixed hook script path handling so prompt audit entries write to `.github\hooks\logs\audit.jsonl` reliably from the configured hook working directory.
- Tightened the dangerous command matching to focus on destructive patterns and added force-push coverage to align the scripts with the workshop explanation.
- Added simple PowerShell helper scripts in `tools\` to turn the demo hook toggle on and off during live sessions.

## 2026-03-17 – Rebalanced context, MCP, and governance workshop chapters

Adjusted the workshop walkthrough so the early narrative teaches durable context first, the MCP chapter showcases the in-repo server directly, and governance explicitly includes the GitHub portal review flow.

### Decisions
- Reworked the context chapter around `AGENTS.md`, `PRD.md`, `specs\`, spec-driven design, constitutions, and Copilot Spaces.
- Removed early hooks and custom-agent emphasis from the first chapter so specialization starts later where it is easier to explain.
- Expanded the MCP chapter with the repository-local `random_string_mcp` server, including implementation details, startup steps, and concrete demo prompts.
- Added explicit pull-request review and security-review guidance in GitHub, tied to repository workflows such as `devskim`, `ossar`, `tfsec`, and `sonarcloud`.
- Corrected MCP docs to describe the local server as a FastMCP SSE server rather than a generic FastAPI demo.

## 2026-03-17 – Rewrote README into a guided workshop script

Adjusted the refreshed README so it reads like a workshop walkthrough for students instead of a meta description of how to present the repo.

### Decisions
- Replaced presenter-oriented wording with chapter-by-chapter instructions aimed at readers following the demo flow.
- Added concrete prompts, files to open, and observations to make each topic easier to demonstrate and understand.
- Kept the main story linear: context -> skills -> MCP -> VS Code agents -> Copilot CLI -> governance -> workflow agents -> SRE.
- Inlined optional demos into the root `README.md` so the workshop can be followed in one place without switching between documents.

## 2026-03-17 – Refreshed workshop assets around custom agents, CLI, hooks, and workflow agents

Updated the workshop repo so the main story is now a presenter-led flow from planning to governed delivery instead of a long feature catalog.

### Decisions
- Rewrote the root `README.md` around a single live-demo journey: context, planning, specialization, Copilot CLI execution, governance, and operations.
- Kept additional demos available without letting them dominate the main walkthrough.
- Added workspace custom agents in `.github/agents/` for planner, integration, deployment, review, and subagent patterns.
- Added reusable prompt files for workshop planning, CLI handoff, governed review, and agentic workflow design.
- Added a simple repository-scoped hooks example in `.github/hooks/` to demonstrate deterministic policy and audit concepts.
- Added `examples/gh-aw/` with source markdown examples for GitHub Agentic Workflows so the story continues beyond coding agents into GitHub Actions governance.
- Updated the English and Czech workshop agendas plus `docs/enterprise_demo_flow.md` so they all reinforce the same presenter-led narrative.

## 2026-03-17 – Removed custom chat mode demo

Removed the deprecated custom chat mode example from the workshop repository so the documentation reflects currently maintained customization paths.

### Decisions
- Deleted the `MyTeacher` custom chat mode artifact from `.github/chatmodes`.
- Removed the `Custom Chat Modes` subsection from the root `README.md`.
- Renumbered the remaining section so `Bring Your Own Model (BYOM)` is now section `3.3`.

## 2026-03-09 – Workshop agenda refocused on agentic delivery

Refreshed the customer workshop agenda to reflect the current GitHub Copilot platform direction.

### Decisions
- Moved the workshop center of gravity from basic editor assistance to agentic end-to-end workflows across VS Code, CLI, and GitHub.
- Elevated GitHub Copilot CLI, `/fleet`, subagents, custom agents, skills, MCP, and spec-driven development from supporting topics to primary agenda items.
- Added explicit coverage for GitHub Agent HQ, cloud and background agents, third-party agents, shared memory, code review, and agentic GitHub Actions workflows.
- Reframed the material around practical customer operating models: context, orchestration, testing, PR-based review, and governance.
- Condensed the final customer-facing agenda into an email-friendly format built around workshop name, short description, and chapter bullets.
- Grounded the refresh in current GitHub and Microsoft guidance around agent mode, Copilot CLI, Agent HQ, Copilot Memory, third-party agents, and GitHub Agentic Workflows.
- Split the final agenda into localized English and Czech variants using `_EN` and `_CZ` suffixes.

## 2025-08-29 – Testing Infrastructure Added

Added unit and integration test scaffolding for `api-processing` and `api-status` services using `pytest`.

### Decisions
- Kept existing `requirements.txt` files; appended test dependencies via documentation instead of migrating to `pyproject.toml` to minimize scope. (A future improvement could consolidate dependency management under a single `pyproject.toml` per service in line with project guidelines.)
- Unit tests isolate business logic with faked Azure SDK clients (Blob, Service Bus, Cosmos) via fixtures in `tests/conftest.py`.
- Integration tests require explicit opt-in using `RUN_INTEGRATION_TESTS=1` and verify real interactions with Azure resources (Blob + Service Bus for processing API, Cosmos DB for status API).
- Adopted `integration` pytest marker; documented usage in READMEs.
 - Dynamic module loading added in tests to support hyphenated directory names (`api-processing`, `api-status`).

### Structure
```
api-processing/
  tests/
    unit/
    integration/
api-status/
  tests/
    unit/
    integration/
```

### Next Possible Improvements
- Introduce `pyproject.toml` + `uv` dependency groups (`[project.optional-dependencies].test`).
- Add GitHub Actions workflow to run unit tests on PR, with optional manual job for integration tests.
- Add more edge case coverage (invalid file types, Cosmos exceptions path, etc.).
- Add contract tests between processing & worker components once worker logic is available.

## 2025-08-29 – Migrated services to uv

Converted `api-processing` and `api-status` from `requirements.txt` + pip to `pyproject.toml` managed by `uv`.

### Changes
- Added `pyproject.toml` for each service with runtime dependencies and `test` optional dependency group.
- Removed legacy `requirements.txt` files.
- Updated READMEs to use `uv sync` and `uv run` commands; documented how to include test extras.
- Ensured existing test suite remains compatible (no code changes required).
 - Added dev dependency list mirroring test extras so `uv sync --dev` also installs test tooling.

### Rationale
Aligns with repository guidance to use `uv` for Python dependency management, improving reproducibility and enabling optional dependency groups.

## 2025-08-31 – Test env loading enhancement

Updated test `conftest.py` in both services to load environment variables from each service's `.env` file before applying fallback defaults. This allows running tests against real Azure resources by just configuring the `.env` without manually exporting variables, while still keeping deterministic defaults for unit tests.

## 2025-08-31 – Simplified integration test trigger

Removed reliance on `RUN_INTEGRATION_TESTS` environment flag. Integration tests are now included only when selected via the pytest marker (`-m integration`). Skips now occur solely on absence of required Azure environment variables. Documentation updated accordingly.

### 2025-08-31 – Integration test skip timing fix
Adjusted integration test modules to load `.env` before evaluating `@pytest.mark.skipif` so that environment variables defined only in the service `.env` file are recognized during collection. Previously the skip condition ran before the autouse fixture loaded `.env`, causing false skips.

