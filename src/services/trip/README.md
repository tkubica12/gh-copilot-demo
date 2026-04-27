# Trip Service

Trip & Gallery Service for the Stuffed Toy World Tour platform.

## Features

- Trip creation with ordered legs (locations, planned arrivals)
- Gallery management (upload/download images per leg)
- Trip status tracking
- Leg status updates
- Owner-based authorization

## Setup

### Prerequisites

- Python 3.12+
- Azure resources provisioned (Cosmos DB, Blob Storage)
- Entra ID app registration
- Valid authentication token

### Configuration

Create `.env` file:

```bash
# Azure Authentication
AZURE_TENANT_ID=your-tenant-id
APP_ID_URI=api://your-app-id

# Cosmos DB
COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_DATABASE_NAME=toytripdb
COSMOS_CONTAINER_NAME=trips

# Blob Storage
STORAGE_ACCOUNT_URL=https://your-account.blob.core.windows.net
BLOB_CONTAINER_GALLERY=gallery

# Inter-service
TOY_SERVICE_URL=http://localhost:8001

# API
API_PORT=8002
LOG_LEVEL=INFO
```

### Install Dependencies

```bash
uv sync
```

### Run Service

```bash
uv run python main.py
```

Service will be available at `http://localhost:8002`.

## API Endpoints

### Trips

- `POST /trip` - Create trip (owner only)
- `GET /trip/{trip_id}` - Get trip details (global)
- `GET /trip?toy_id={id}` - List trips by toy (global)
- `GET /trip?owner_oid={oid}` - List trips by owner (global)
- `PATCH /trip/{trip_id}` - Update trip (owner only)
- `DELETE /trip/{trip_id}` - Delete trip (owner only)

### Gallery

- `POST /trip/{trip_id}/gallery` - Upload image (owner only)
- `GET /trip/{trip_id}/gallery/{image_id}` - Download image (global)
- `DELETE /trip/{trip_id}/gallery/{image_id}` - Delete image (owner only)

### Leg Status

- `PATCH /trip/{trip_id}/legs/{leg_number}/status` - Update leg status (owner only)

### Monitoring

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics endpoint

## Metrics

The service exposes Prometheus metrics at `/metrics`:

- `trip_service_http_requests_total` - Total HTTP requests (labels: method, endpoint, status)
- `trip_service_http_request_duration_seconds` - Request latency histogram (labels: method, endpoint)
- `trip_service_trips_created_total` - Total trips created
- `trip_service_trips_updated_total` - Total trips updated
- `trip_service_trips_deleted_total` - Total trips deleted
- `trip_service_photos_uploaded_total` - Total photos uploaded
- `trip_service_active_trips` - Current number of active trips

See `deploy/MONITORING.md` for Grafana dashboard setup.

## Testing

Integration tests are in `src/integration-tests/test_trip_integration.py`.

```bash
cd ../../integration-tests
uv run pytest test_trip_integration.py -v
```
