# API status

This API provides the status and results of processed images stored in Azure Cosmos DB.

## Components Used
- Azure Cosmos DB (reading results)
- Azure Monitor (monitoring and logging)
- Prometheus (metrics exposure)

## Prometheus Metrics

The service exposes Prometheus metrics at `/metrics` endpoint.

### Available Metrics
- `http_requests_total` - Total HTTP requests by method, handler, and status
- `http_request_duration_seconds` - HTTP request duration histogram
- `http_request_size_bytes` - HTTP request size
- `http_response_size_bytes` - HTTP response size
- `http_requests_in_progress` - Current number of requests being processed

### Testing Metrics Locally

Start the service:
```bash
uv sync
uv run uvicorn main:app --port 8081
```

Access metrics:
```bash
curl http://localhost:8081/metrics
```

Make a few requests to generate metrics:
```bash
# Generate some traffic
for i in {1..10}; do
  curl http://localhost:8081/api/status/test-guid-123
done

# Check metrics again
curl http://localhost:8081/metrics | grep http_requests_total
```

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

