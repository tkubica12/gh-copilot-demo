# Agent Development Guidelines

## 1. Purpose

Provide a clear, single reference for implementing, extending, and maintaining AI agents and related services in this repository.

## 2. Core Principles

1. **Simplicity First**: This project is designed for learning. Strive for simplicity and avoid complicated or premature abstractions.
2. **Self-Documenting Code**: Keep functionality self‑documenting; use docstrings, not progress/status comments.
3. **Cohesion**: Minimize surface area: small, cohesive modules > large monoliths.
4. **Explicitness**: Explicit > implicit for data contracts, configuration, and side effects.
5. **Disposable Experiments**: Make cheap experiments disposable (prefixed `adhoc_`), not permanent.
6. **Basic Security**: It is OK to start with basic security for learning speed, but always document next steps for production hardening.
7. **Simple Deployment**: Simple deployment setups without HA are acceptable for this learning environment.

## 3. Project‑Wide Conventions

### 3.1 Documentation
* **Specs Structure**:
    * `specs/platform/`: Cross-cutting concerns (Architecture, Data Models, Security).
    * `specs/services/<service>/`: Service-specific specs (API, Testing, Deployment).
* **Docstrings**: Primary documentation channel inside code (revise whenever code changes).
* **Comments**: Only for non‑obvious logic. No progress logs or "previous implementation" notes.
* **Implementation Log**: Update `docs/ImplementationLog.md` with meaningful technical decisions.
* **Common Errors**: Add confirmed recurring pitfalls to `docs/CommonErrors.md` (after user confirmation).
* **README**: Each component/service keeps concise run & test instructions in its local `README.md`.

### 3.2 Refactoring & Improvements
* Perform low‑risk, obviously beneficial cleanups directly.
* For broader architectural shifts, surface a brief rationale in chat before proceeding.

### 3.3 Experiments & Troubleshooting
* Consult `docs/CommonErrors.md` first.
* Use `adhoc_` prefix for disposable scripts.

### 3.4 Technology Stack

#### Python (Key Insights)
* **Version**: Target Python 3.11+.
* **Style**: Follow PEP 8. Max line length 100 chars. `snake_case` for functions/vars, `PascalCase` for classes. Type hints everywhere.
* **Dependencies**: Use `pip` with `requirements.txt` (or `uv` if configured). Pin dependencies.
* **Logging**: Use standard `logging`. No `print` statements in production.
* **Testing**: Use `pytest`. Unit tests for logic, integration tests for IO.
* **Security**: Load secrets from `.env`. Validate inputs via Pydantic.

#### Terraform (Key Insights)
* **Version**: Use latest stable Terraform. Pin versions.
* **Providers**: Use `azurerm` for standard resources, `azapi` for bleeding-edge.
* **Structure**: Segment resources by type (`networking.tf`, `rbac.tf`). Keep `main.tf` for config.
* **Variables**: Rich descriptions, specific types.
* **State**: Remote state (e.g., Azure Storage). State locking.
* **Security**: No hardcoded secrets. Use Key Vault or env vars.

## 4. Service Guidelines (Python)

### 4.1 Structure & Modeling
* **Layout**: Modular structure (`models/`, `routes/`, `services/`, `utils/`).
* **Entry Point**: `main.py` for application entry.
* **Config**: `config.py` for env vars and settings.

### 4.2 Documentation & Style
* Docstrings for every public class/function.
* Avoid redundant comments.

### 4.3 Logging
* Log at INFO for lifecycle, DEBUG for diagnostics, WARNING for anomalies, ERROR for failures.

### 4.4 Testing
* `pytest` with descriptive names.
* Mock repositories for unit tests.
* Integration tests for persistence/API.

## 5. Infrastructure as Code (Terraform)

### 5.1 Project Structure
* Split resources into logical files.
* Use `variables.tf` and `outputs.tf`.

### 5.2 Coding Conventions
* **Variables**: Multi-line descriptions, sensible defaults.
* **Naming**: `snake_case` for resources.
* **Comments**: Only for non-obvious attributes.

### 5.3 State Management
* Remote backend (Azure Storage).
* Separate state for environments if applicable.

## 6. Reinforced Documentation & Logging Rules

1. **Implementation Log**: Update `docs/ImplementationLog.md` autonomously.
2. **Architecture Decisions**: Propose ADRs for fundamental changes.
3. **Common Errors**: Consult and propose additions to `docs/CommonErrors.md`.
4. **No Progress Comments**: Ban inline comments like "// updated logic".

## 7. Ad‑Hoc / Disposable Artifacts

| Type | Naming Pattern | Purpose | Lifecycle |
|------|----------------|---------|-----------|
| Scratch test | `adhoc_test_*.py` | Quick reproduction | Delete after insight |
| Doc draft | `ADHOC_*.md` | Staging for docs | Merge and delete |

## 8. Change Control & Communication

1. Summarize intent/risk before major changes.
2. Update docstrings and logs after implementation.
3. Propose remediation for systemic flaws.

## 9. Quick Reference Checklist

1. Define/confirm data contract.
2. Write/extend tests.
3. Implement feature (docstrings maintained).
4. Run tests.
5. Update `README.md`.
6. Log decision in `ImplementationLog.md`.
7. Remove `adhoc_` artifacts.

## 10. Scope & Precedence

1. Explicit user instruction overrides this file.
2. `specs/` documentation governs architecture.
3. This file governs daily engineering discipline.
