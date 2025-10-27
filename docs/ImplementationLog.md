# Implementation Log

## 2025-10-10 – Completed uv migration for all Python services

Completed the migration of all Python services (`api-processing`, `api-status`, and `worker`) to use `uv` as package manager with `pyproject.toml` as the authoritative dependency source.

### Changes
- **api-processing** and **api-status**: Already had `pyproject.toml` but still referenced `requirements.txt` in older implementation log. Generated frozen `requirements.txt` from `pyproject.toml` using `uv pip compile` for Docker builds.
- **worker**: Created new `pyproject.toml` with all dependencies. Generated `requirements.txt` from it for Docker builds.
- Updated all service READMEs with comprehensive uv dependency management instructions.
- Replaced deprecated `[tool.uv].dev-dependencies` with standard `[dependency-groups].dev` in api-processing and api-status.
- Verified `uv sync` works correctly for all services.

### Rationale
Docker builds in CI/CD environments can encounter network/SSL issues when using uv directly. By generating `requirements.txt` files from `pyproject.toml` using `uv pip compile`, we maintain the benefits of uv for local development while ensuring reliable Docker builds using standard pip.

Developers use `uv sync` for local development, and when dependencies change in `pyproject.toml`, they regenerate `requirements.txt` with `uv pip compile pyproject.toml -o requirements.txt`.

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

