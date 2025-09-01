# Implementation Log

## 2025-01-XX – Worker Unit Tests and CI Integration Added

Added comprehensive unit testing infrastructure for the worker service and integrated tests into the CI/CD pipeline.

### Decisions
- Migrated worker from `requirements.txt` to `pyproject.toml` to align with project guidelines for dependency management using `uv`
- Created unit tests that mock all Azure dependencies (Service Bus, Blob Storage, Cosmos DB, OpenAI) to test business logic in isolation
- Added CI test step in GitHub Actions workflow that runs tests before container build to prevent deployment of failing code
- Tests cover environment variable validation, message processing logic, error handling, and edge cases
- Used dynamic module loading pattern consistent with other services to handle module imports in tests

### Structure
```
worker/
  tests/
    unit/
      test_worker.py
    conftest.py
  pyproject.toml
  main.py
  README.md (updated with test documentation)
```

### Test Coverage
- Environment variable validation (`get_env_var` function)
- Successful message processing workflow
- Error handling for invalid JSON messages
- OpenAI API exception handling
- Cosmos DB exception handling
- Missing message fields handling

### CI Integration
- Added `test` job in worker-BUILD.yml workflow that runs before `build-and-push`
- Tests are run with verbose output and fail fast to provide quick feedback
- Container build only proceeds if all tests pass

### Files Modified
- `worker/pyproject.toml` - Created with runtime and test dependencies
- `worker/tests/conftest.py` - Test fixtures with mocked Azure services
- `worker/tests/unit/test_worker.py` - Comprehensive unit tests
- `worker/README.md` - Updated with test documentation and running instructions
- `worker/Dockerfile` - Updated to use pyproject.toml dependencies
- `.github/workflows/worker-BUILD.yml` - Added test step before build
- `worker/requirements.txt` - Removed (migrated to pyproject.toml)

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

