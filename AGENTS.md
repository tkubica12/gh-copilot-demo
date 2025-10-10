# Agent Development Guidelines

## 1. Purpose

Provide a clear, single reference for implementing, extending, and maintaining AI agents and related services (Python backends, data scripts, infra IaC, frontend interactions) in this repository.

## 2. Core Principles

1. Favor simplicity and readability over premature abstraction.
2. Keep functionality self‑documenting; use docstrings, not progress/status comments.
3. Minimize surface area: small, cohesive modules > large monoliths.
4. Explicit > implicit for data contracts, configuration, and side effects.
5. Make cheap experiments disposable (prefixed `adhoc_`), not permanent.

## 3. Project‑Wide Conventions

### 3.1 Documentation
* Primary documentation channel inside code: **docstrings** (revise them whenever code changes behavior or signature).
* Only add code comments for non‑obvious logic or critical nuances. Never for progress logs, migration notes, or “previous implementation” commentary.
* Update `docs/ImplementationLog.md` with meaningful architectural or technical decisions (not micro‑steps) when a feature is completed or a design choice is finalized.
* Add confirmed recurring pitfalls to `docs/CommonErrors.md` (after user confirmation—see Section 6).
* Each component/service keeps concise run & test instructions in its local `README.md`.

### 3.2 Refactoring & Improvements
Opportunistic simplifications are encouraged. When you see a refactor beyond the immediate task:
* Perform low‑risk, obviously beneficial cleanups directly (pure simplification, dead code removal).
* For broader architectural shifts, surface a brief rationale in chat before proceeding.

### 3.3 Experiments & Troubleshooting
When investigating complex issues:
1. Prefer quick inline or REPL tests first.
2. Use PowerShell friendly commands (Windows dev baseline).
3. Load environment variables from `.env` when relevant.
4. If a throwaway script is necessary, name it `adhoc_test_<purpose>.py` (see Section 7) and delete after insights are integrated.

### 3.4 Technology Stack
* Primary backend language: **Python**, package & env management via `uv` (`pyproject.toml` authoritative; avoid `requirements.txt`).
* API framework: **FastAPI**.
* Data validation: **Pydantic** models (under `models/`).
* Frontend: **React** + `assistant-ui` (Tailwind present).

## 4. Python Agent & Service Guidelines

### 4.1 Structure & Modeling
* Use Pydantic models for request/response & internal validated schemas. Place in `models/`.
* Keep service boundaries explicit (e.g., `routes/`, `services/`, `repositories/`).

### 4.2 Documentation & Style
* Every public class/function: docstring specifying purpose, parameters, return value(s), exceptions.
* Avoid redundant comments explaining obvious code or restating names.

### 4.3 Logging
* Use Python `logging` with appropriate levels: DEBUG (diagnostics), INFO (lifecycle events), WARNING (recoverable anomalies), ERROR (failures), CRITICAL (systemic outages).
* No print statements in production paths.

### 4.4 Testing
* Use `pytest`.
* Prefer unit tests (mocks) for logic; integration tests for IO (DB, external HTTP, vector stores, etc.).
* If a one‑off exploratory script was needed, port validated findings into tests and delete the ad‑hoc script.

### 4.5 Ports & Local Dev
* Assign distinct default ports per service to avoid collisions (document them in the service `README.md`).

## 5. Infrastructure as Code

### 5.1 Providers
* Use `azurerm` for standard Azure resources.
* Use `azapi` for bleeding‑edge features unsupported in `azurerm`.

### 5.2 File Organization
Segment resource types: `networking.tf`, `service_bus.tf`, `rbac.tf`, etc. If a type bloats, split further: `container_app.frontend.tf`, `container_app.backend.tf`.

### 5.3 Variables
* Always include rich multi‑line descriptions: purpose, type, constraints, examples.
* Provide sensible defaults where safe.

### 5.4 Comments
* Only for non‑obvious attributes or critical justification. No change logs, no progress notes.

### 5.5 Tags
* Tags optional unless explicitly requested.

## 6. Reinforced Documentation & Logging Rules (Augmented Requirements)

These constraints exist to prevent uncontrolled documentation sprawl and progress leakage into code:

1. Implementation Log Boundaries: Implementation progress, rationale, or “this replaces X” notes belong in `docs/ImplementationLog.md`—never as inline code comments or new files.
2. Common Errors Workflow: Only after confirming with the user that an issue is broadly relevant, add it to `docs/CommonErrors.md`. Do not create parallel error collections.
3. Controlled Design Changes: Architectural or behavioral design alterations should be reflected (after approval) in `docs/SolutionDesign.md`. Treat `SolutionDesign.md` as a guiding artifact; do not mutate it unilaterally.
4. Localized Documentation First: Prefer updating the affected component’s `README.md` for usage/run/test changes before touching high‑level design docs.
5. Tests over Scratch Scripts: Validate behaviors via `pytest` (unit/integration). Temporary investigative scripts must follow Section 7 and be removed post‑learning.
6. Communication Channel Priority: To inform about implementation decisions use (a) chat output, (b) component `README.md` (brief), (c) `SolutionDesign.md` (after approval). Do not introduce new permanent doc files unless genuinely required.
7. New Doc File Exception: If a truly new doc artifact is justified, prefix filename with `ADHOC_` and notify user. Expect eventual consolidation or deletion.
8. No Progress/History Comments: Ban inline comments like “// updated previous logic” or “# temporary hack (will remove)”—instead record durable decisions in `ImplementationLog.md`.

## 7. Ad‑Hoc / Disposable Artifacts

| Type | Naming Pattern | Purpose | Lifecycle |
|------|----------------|---------|-----------|
| Python scratch test | `adhoc_test_*.py` or `adhoc_*.py` | Quick reproduction / isolate behavior | Delete after converting insight into real tests/code |
| Documentation draft | `ADHOC_*.md` | Rare: staging ground for large doc refactor | Merge content into canonical doc then delete |

Rules:
* Must not be imported by production code.
* Must not hold secrets or credentials.
* Track none of them in long‑term design history; only distilled results.

## 8. Change Control & Communication

1. Before major architectural changes: summarize intent, risk, alternatives in chat for approval.
2. After implementing a feature: update relevant docstrings + (if needed) `ImplementationLog.md`.
3. If you discover systemic flaw: propose remediation path; avoid broad speculative refactors without confirmation.

## 9. Quick Reference Checklist

Development Flow:
1. Define/confirm data contract (Pydantic model). 
2. Write/extend tests (failing first where feasible).
3. Implement feature (docstrings maintained—no progress comments).
4. Run `pytest` (unit + integration if relevant).
5. Update service `README.md` for operational changes.
6. Log architectural decision in `ImplementationLog.md` if strategic.
7. Remove any `adhoc_` artifacts created during exploration.

Terraform Flow:
1. Place resource in appropriate file (create or extend). 
2. Add rich variable descriptions and smart defaults.
3. Limit comments to non‑obvious attributes.

Ad‑Hoc Script Flow:
1. Name with `adhoc_` prefix. 
2. Isolate experiment. 
3. Migrate result into tests or code. 
4. Delete script.

## 10. Scope & Precedence

This `AGENTS.md` centralizes operational & stylistic guidance. If conflicts arise:
1. Explicit user instruction (chat) overrides this file case‑by‑case.
2. `SolutionDesign.md` governs architecture (pending approved changes).
3. This file governs daily engineering discipline & hygiene.
