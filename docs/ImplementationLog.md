# Implementation Log

## 2026-03-17 – Terraform demo infrastructure README added

Added a detailed README under `examples/terraform/` documenting the Azure infrastructure stack, resource inventory, variables, deployment flow, and operational caveats for the demo Container Apps environment.

### Decisions
- Documented the Terraform folder as a self-contained Azure deployment centered on Container Apps, Storage, Service Bus, Cosmos DB, monitoring, and managed identity.
- Included a resource-by-resource inventory and variable reference so the folder can be understood without reading every `.tf` file first.
- Documented deployment options for the existing hardcoded AzureRM backend and for reconfiguration when deploying to a different subscription or state account.
- Called out demo-grade security and operability gaps such as checked-in secrets, wildcard CORS, lack of outputs, and limited networking hardening.

## 2026-03-09 – Customer-facing chapter structure added under `docs/`

Added a concise six-chapter workshop structure under `docs/` so the main repository guide can stay shorter and link into focused customer-facing material.

### Decisions
- Added numbered chapter docs for basics, agentic delivery, context, skills and MCP, Agent HQ orchestration, and governed delivery.
- Kept existing deep-dive docs in place and positioned the new chapter docs as entry points that link to more specialized material instead of duplicating it.
- Moved GitHub Spark into the basics narrative so it works as an accessible on-ramp rather than a separate adjacent chapter.
- Moved Azure SRE Agent into governed delivery so coding, workflow agents, and operations all share one governance-centered closing story.

## 2026-03-09 – Governed workflow-agent examples added

Added illustrative GitHub Actions workflow-agent examples and supporting governance guidance so the repo can tell a more modern enterprise story around GitHub Agentic Workflows.

### Decisions
- Added two manual, clearly labeled demo workflows that generate markdown-authored briefing artifacts rather than attempting unattended agent execution.
- Positioned workflow agents as complements to the repo's existing CI/CD, security scanning, and deployment workflows instead of replacements.
- Documented guidance around approvals, auditability, runtime budgets, security review, and code quality expectations.
- Kept permissions read-only in the demo workflows to model least privilege for advisory and review-oriented agentic automation.

## 2026-03-09 – README reorganized around chapter-linked workshop flow

Shortened the main README and turned it into a clean workshop map that links into chapter docs and deep dives instead of trying to carry the full story inline.

### Decisions
- Moved the primary workshop narrative into numbered chapter docs under `docs/` so each major topic has room for a deeper explanation.
- Reframed the main README as a concise customer-facing guide to the workshop flow: basics, agentic delivery, context, skills and MCP, Agent HQ, and governed delivery.
- Linked custom agents, subagents, Copilot CLI, workflow agents, Spark, and Azure SRE Agent from the main entry point so the overall structure is easy to navigate.

## 2026-03-09 – Workshop docs simplified into clean chapter guides

Removed numbered chapter filenames and folded the extra deep-dive split back into cleaner chapter-oriented guides.

### Decisions
- Renamed the main workshop chapter docs to clean descriptive names such as `basics.md`, `agentic-delivery.md`, and `governed-delivery.md`.
- Folded key Copilot CLI, Agent HQ, and workflow-agent guidance back into the chapter guides so the workshop path stays easier to follow.
- Simplified the main README so every chapter explains what it is, why it matters, and where to go next.

## 2026-03-09 – `.github` assets aligned to an agent-first workshop

Refreshed the repository customization assets so the demo better reflects modern GitHub Copilot usage built around `AGENTS.md`, custom agents, skills, prompts, chat modes, and orchestration patterns.

### Decisions
- Added a compact set of custom agents for orchestration, planning and handoff, implementation, and review instead of leaving `.github/agents/` empty.
- Replaced legacy prompts and chat mode examples with assets centered on planning, handoff packets, `/fleet`, and choosing between `AGENTS.md`, custom agents, skills, and MCP.
- Added explicit skills guidance that positions skills as reusable local workflow or domain capabilities and MCP as the bridge to live remote systems.
- Added a workshop-patterns skill to make planning, delegation, and parallelization guidance reusable inside the repository.
- Kept the examples practical and concise so they are easy to demo without introducing an oversized framework.

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
