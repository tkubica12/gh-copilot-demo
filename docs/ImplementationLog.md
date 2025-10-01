# Implementation Log

## 2025-01-XX – Prometheus Metrics and Grafana Monitoring Added

Added Prometheus metrics endpoints to all microservices and configured Azure Monitor Workspace with Managed Grafana for monitoring.

### Changes
- **API Services (api-processing, api-status)**: Added `prometheus-fastapi-instrumentator` library to expose `/metrics` endpoint with HTTP request metrics (total requests, duration histograms, status codes)
- **Worker Service**: Added `prometheus-client` library with custom metrics:
  - `worker_messages_processed_total`: Count of successfully processed messages
  - `worker_messages_failed_total`: Count of failed messages
  - `worker_message_processing_seconds`: Processing duration histogram
  - `worker_queue_depth`: Current queue depth gauge
  - `worker_openai_api_seconds`: OpenAI API call duration histogram
- **Infrastructure**: Added Azure Monitor Workspace and Azure Managed Grafana to Terraform
- **Container App Environment**: Configured OpenTelemetry integration to send metrics to Azure Monitor Workspace
- **Grafana Dashboards**: Created service-specific dashboards in `grafana-dashboards/` directory:
  - `api-processing.json`: Request rate, response times, error rates
  - `api-status.json`: Request rate, response times, status distribution
  - `worker.json`: Message processing metrics, queue depth, OpenAI API performance

### Architecture Decisions
- Used `prometheus-fastapi-instrumentator` for FastAPI services as it provides automatic instrumentation with minimal code changes
- Worker service uses standard `prometheus-client` with custom metrics since it's not a web service
- Metrics exposed on default ports (FastAPI services on their main port, worker on port 8000)
- Integrated with existing Azure Monitor/Application Insights setup for comprehensive observability

### Testing
- Verified `/metrics` endpoint functionality for both API services locally
- Confirmed metrics format is Prometheus-compatible

### Next Steps
- Deploy infrastructure changes and verify metrics collection in Azure Monitor Workspace
- Import Grafana dashboards and configure data sources
- Consider adding alerting rules based on key metrics (error rates, processing times, queue depth)

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

