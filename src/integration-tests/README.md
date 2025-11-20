# Integration Tests

End-to-end integration tests for ToyTrips microservices with real authentication and Azure resources.

## Purpose

Integration tests verify complete service flows with:
- **Real authentication** - Uses tokens from Entra ID (not mocked)
- **Real Azure resources** - Cosmos DB, Blob Storage, Service Bus
- **Real authorization** - Ownership checks, role validation
- **Cross-service interactions** - Tests that span multiple services

## Differences from Unit Tests

| Aspect | Unit Tests (in service folders) | Integration Tests (here) |
|--------|--------------------------------|-------------------------|
| **Speed** | Fast (milliseconds) | Slower (seconds) |
| **Dependencies** | Mocked | Real Azure resources |
| **Authentication** | Mocked principals | Real Entra ID tokens |
| **Isolation** | High (no external calls) | Low (network, database) |
| **When to run** | Every commit | Before merge/deploy |
| **Purpose** | Verify logic correctness | Verify system integration |

## Prerequisites

### 1. Create App Registration

```bash
cd tools/identity
python create_app_registration.py --name "ToyTrips-Dev"
```

This creates `app_registration.json` with app details.

### 2. Configure Services

Update service `.env` files with values from `app_registration.json`:

```bash
# src/services/toy/.env
TENANT_ID=<tenant_id>
APP_ID_URI=<identifier_uri>
COSMOS_ENDPOINT=<your_cosmos_endpoint>
COSMOS_DATABASE_NAME=toytrips
COSMOS_CONTAINER_NAME=toys
STORAGE_ACCOUNT_URL=<your_storage_url>
BLOB_CONTAINER_AVATARS=avatars
```

### 3. Get Authentication Token

```bash
cd tools/identity
python get_auth_token.py
```

This creates `auth_token.json` with a valid token for testing.

### 4. Start Services

```bash
# Terminal 1: Toy service
cd src/services/toy
uv run uvicorn main:app --reload --port 8000

# Terminal 2 (future): Trip service
# cd src/services/trip
# uv run uvicorn main:app --reload --port 8001
```

## Running Tests

### Run all integration tests

```bash
cd src/integration-tests
uv run pytest -v
```

### Run specific test file

```bash
uv run pytest test_toy_integration.py -v
```

### Run tests with specific markers

```bash
# Only authentication tests
uv run pytest -m auth -v

# Skip slow tests
uv run pytest -m "not slow" -v
```

### Run with detailed output

```bash
uv run pytest -v -s  # -s shows print statements
```

## Environment Variables

Create `.env` in this folder for configuration:

```bash
# Service URLs
TOY_SERVICE_URL=http://localhost:8000
TRIP_SERVICE_URL=http://localhost:8001
ADDON_SERVICE_URL=http://localhost:8002

# Optional: Override token path
AUTH_TOKEN_PATH=../../tools/identity/auth_token.json
```

## Test Structure

```
integration-tests/
├── conftest.py              # Shared fixtures (auth, cleanup, config)
├── test_toy_integration.py  # Toy service tests
├── test_trip_integration.py # Trip service tests (future)
└── test_cross_service.py    # Multi-service flows (future)
```

## Writing New Integration Tests

### Basic Test Template

```python
import httpx
import pytest

@pytest.mark.integration
@pytest.mark.auth
class TestMyServiceIntegration:
    
    @pytest.mark.usefixtures("check_services_available")
    def test_my_feature(
        self, 
        service_config: dict, 
        auth_headers: dict, 
        cleanup_toys: list
    ):
        """Test description."""
        base_url = service_config["toy_service_url"]
        
        # Make authenticated request
        response = httpx.post(
            f"{base_url}/toy",
            json={"name": "Test"},
            headers=auth_headers,
            timeout=10.0
        )
        
        assert response.status_code == 201
        toy_id = response.json()["id"]
        cleanup_toys.append(toy_id)  # Automatic cleanup
```

### Available Fixtures

- `auth_token` - Token data from `auth_token.json`
- `auth_headers` - Headers dict with Authorization bearer token
- `service_config` - Service URLs from environment
- `user_oid` - Current user's OID from token
- `cleanup_toys` - List for automatic toy cleanup after test
- `check_services_available` - Skips test if services not running

## Token Management

Tokens expire after ~1 hour. If tests fail with 401:

```bash
cd tools/identity
python get_auth_token.py  # Refresh token
cd ../../src/integration-tests
uv run pytest -v  # Re-run tests
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Integration Tests
  env:
    TOY_SERVICE_URL: ${{ secrets.TOY_SERVICE_URL }}
    # Token obtained via service principal in CI
  run: |
    cd src/integration-tests
    uv run pytest -m integration -v
```

## Troubleshooting

### "Authentication token not found"

Run: `python tools/identity/get_auth_token.py`

### "Authentication token expired"

Tokens expire after ~1 hour. Re-run: `python tools/identity/get_auth_token.py`

### "Required services not available"

Ensure services are running on expected ports (check `service_config`)

### 401 Unauthorized

- Verify token is valid (check `auth_token.json` expires_on)
- Ensure service configuration has correct `TENANT_ID` and `APP_ID_URI`
- Check service logs for validation errors

### 403 Forbidden

- User may not have required role assigned
- Go to Azure Portal → Enterprise Applications → Your App → Users and groups
- Assign user to `Toy.ReadWrite` role

### Tests hang or timeout

- Increase timeout: `httpx.get(url, timeout=30.0)`
- Check service logs for errors
- Verify Azure resources (Cosmos, Storage) are accessible

## Best Practices

1. **Always use cleanup fixtures** - Prevent test data accumulation
2. **Use realistic test data** - Similar to production payloads
3. **Test error paths** - Not just happy path
4. **Mark slow tests** - Use `@pytest.mark.slow` for tests >5s
5. **Document prerequisites** - Especially for complex multi-step tests
6. **Use descriptive names** - Test name should explain what's verified
7. **Verify side effects** - Check database/blob changes, not just HTTP status

## Future Enhancements

- [ ] Multi-user testing (second user token for ownership tests)
- [ ] Performance/load testing variants
- [ ] Cross-service transaction tests (trip + addon flow)
- [ ] WebSocket live streaming tests (geo service)
- [ ] Story generation batch tests
- [ ] Test data seeding utilities
