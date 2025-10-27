# Implementation Log

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

## 2025-10-14 – API Processing Service Performance Optimization

Converted `api-processing` service from synchronous to asynchronous Azure SDK clients to eliminate blocking I/O operations and improve concurrent request handling.

### Root Cause
The endpoint was defined as `async def` but performed synchronous I/O operations (`container_client.upload_blob()` and `servicebus_queue.send_messages()`), blocking the async event loop and preventing efficient concurrent request processing.

### Changes
- Migrated from sync to async Azure SDK clients: `azure.storage.blob.aio.BlobServiceClient` and `azure.servicebus.aio.ServiceBusClient`
- Updated blob upload to use `await container_client.upload_blob()`
- Changed Service Bus message sending to use async context manager with `await sender.send_messages()`
- Implemented FastAPI lifespan context manager for proper async client initialization and cleanup
- Added `aiohttp` dependency required for async Azure SDK transport
- Updated test fixtures to mock async client methods

### Performance Impact
- Eliminates blocking operations that prevented concurrent request handling
- Enables true asynchronous I/O throughout the request pipeline
- Expected significant improvement in throughput and p95 latency under load
- Better resource utilization through non-blocking operations

### Testing
All unit tests pass with updated async mocks. Integration tests remain available for validation against real Azure resources.

