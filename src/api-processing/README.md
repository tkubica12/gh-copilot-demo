# API processing

This API accepts image uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at `/api/process`.

## Performance Optimization

The service uses **async Azure SDK clients** (`azure.storage.blob.aio` and `azure.servicebus.aio`) to enable true asynchronous I/O operations. This allows the service to handle multiple concurrent requests efficiently without blocking the event loop, significantly improving throughput and reducing response latency under load.

Key optimizations:
- Async blob upload to Azure Storage
- Async message sending to Service Bus
- Proper async context management with FastAPI lifespan events
- Non-blocking I/O operations throughout the request pipeline

## Components Used
- Azure Storage Blob (storing images)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)

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

