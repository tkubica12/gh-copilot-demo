# API status

This API provides the status and results of processed images stored in Azure Cosmos DB.

## Components Used
- Azure Cosmos DB (reading results)
- Azure Monitor (monitoring and logging)
- Prometheus (metrics)

## Metrics

The service exposes Prometheus metrics at the `/metrics` endpoint, including:
- HTTP request counts by method, path, and status code
- Request duration histograms
- HTTP requests in progress

## Tests
Structure mirrors the processing service:

- `tests/unit` – unit tests with a fake Cosmos container (no network access).
- `tests/integration` – requires real Cosmos DB; skipped unless `RUN_INTEGRATION_TESTS=1`.

### Install dependencies (uv)
Base deps (runtime only):
```
uv sync
```
Add test dependencies (choose one):
```
uv sync --extra test
# OR
uv sync --dev
```

### Run unit tests only
```
uv run pytest -m "not integration" -v
```

### Run integration tests
Set environment variables: `COSMOS_ACCOUNT_URL`, `COSMOS_DB_NAME`, `COSMOS_CONTAINER_NAME`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `RETRY_AFTER` then run:
```
uv run pytest -m integration -v
```

### Run all tests
```
uv run pytest -v
```

### Markers
`integration` – real Azure calls (run explicitly with `-m integration`).

Unit test fakes are defined in `tests/conftest.py`.

