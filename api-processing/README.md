# API processing

This API accepts image uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at `/api/process`.

## Components Used
- Azure Storage Blob (storing images)
- Azure Service Bus (sending messages)
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
uv run uvicorn main:app --port 8080
```

Access metrics:
```bash
curl http://localhost:8080/metrics
```

Make a few requests to generate metrics:
```bash
# Generate some traffic
for i in {1..10}; do
  curl -X POST http://localhost:8080/api/process -F "file=@example.jpg"
done

# Check metrics again
curl http://localhost:8080/metrics | grep http_requests_total
```

## Tests
We distinguish **unit** and **integration** tests:

- Unit tests (under `tests/unit`) run fast, have no external side‑effects and mock all Azure dependencies.
- Integration tests (under `tests/integration`) talk to real Azure resources (blob + Service Bus). They are **skipped by default**.

### Install dependencies (uv)
Sync base dependencies (runtime only):
```
uv sync
```
Include test dependencies (choose one):
```
uv sync --extra test          # use optional dependency group
# OR install dev deps (duplicates for convenience)
uv sync --dev
```

### Run unit tests only
```
uv run pytest -m "not integration" -q
```

### Run integration tests
Ensure required environment variables point to test resources, then:
```
uv run pytest -m integration -q
```

Required variables: `STORAGE_ACCOUNT_URL`, `STORAGE_CONTAINER`, `SERVICEBUS_FQDN`, `SERVICEBUS_QUEUE`, `PROCESSED_BASE_URL`, `APPLICATIONINSIGHTS_CONNECTION_STRING`.

### Run all tests
```
uv run pytest -q
```

### Markers
`integration` – real Azure calls (run explicitly with `-m integration`).

---
Tests use `pytest` fixtures in `tests/conftest.py` to inject fakes for Azure SDK clients during unit testing.

