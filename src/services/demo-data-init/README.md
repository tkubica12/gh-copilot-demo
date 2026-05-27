# Demo Data Init Service

Admin-only FastAPI service that reseeds toy and trip demo content on demand.

## Features

- `POST /demo-data/import` runs an import immediately and returns per-run stats
- Authorization enforced via Entra ID bearer token with the `Admin.FullAccess` app role
- Downstream toy/trip service calls reuse the caller's token for auditing

## Local development

```bash
uv sync
uv run fastapi dev main.py
```

Set the following environment variables or `.env` entries:

- `AZURE_TENANT_ID`
- `APP_ID_URI`
- `TOY_SERVICE_URL`
- `TRIP_SERVICE_URL`
- `DEMO_DATA_ROLE_VALUE` (defaults to `Admin.FullAccess`)

Assets default to `../tools/data` so make sure that repository path exists locally.

## API Endpoints

- `POST /demo-data/import` - Trigger data import (admin only)
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics endpoint

## Metrics

The service exposes Prometheus metrics at `/metrics`:

- `demo_data_init_http_requests_total` - Total HTTP requests (labels: method, endpoint, status)
- `demo_data_init_http_request_duration_seconds` - Request latency histogram (labels: method, endpoint)
- `demo_data_init_import_operations_total` - Total import operations (labels: status)
- `demo_data_init_toys_imported_total` - Total toys imported
- `demo_data_init_trips_imported_total` - Total trips imported
- `demo_data_init_photos_imported_total` - Total photos imported

See `deploy/MONITORING.md` for Grafana dashboard setup.
