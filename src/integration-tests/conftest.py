"""
Pytest configuration and shared fixtures for integration tests.

Provides:
- Real authentication fixtures using tokens from tools/identity/auth_token.json
- Azure resource fixtures for tests requiring real dependencies
- Shared test data and cleanup utilities
"""

import json
import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add shared modules to path
shared_path = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(shared_path))


@pytest.fixture(scope="session")
def auth_token() -> dict:
    """
    Load authentication token from tools/identity/auth_token.json.
    
    Run tools/identity/get_auth_token.py first to generate the token.
    """
    token_path = Path(__file__).parent.parent.parent / "tools" / "identity" / "auth_token.json"
    
    if not token_path.exists():
        pytest.skip(
            "Authentication token not found. "
            "Run: python tools/identity/get_auth_token.py"
        )
    
    with open(token_path) as f:
        token_data = json.load(f)
    
    # Check if token is still valid (basic check)
    import time
    if token_data.get("expires_on", 0) < time.time():
        pytest.skip(
            "Authentication token expired. "
            "Run: python tools/identity/get_auth_token.py"
        )
    
    return token_data


@pytest.fixture
def auth_headers(auth_token: dict) -> dict[str, str]:
    """
    Generate authorization headers for HTTP requests.
    
    Usage:
        response = httpx.get(url, headers=auth_headers)
    """
    return {
        "Authorization": f"Bearer {auth_token['token']}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def service_config() -> dict:
    """
    Load service configuration from environment.
    
    Required environment variables:
    - TOY_SERVICE_URL (default: http://localhost:8001)
    - TRIP_SERVICE_URL (default: http://localhost:8002)
    """
    return {
        "toy_service_url": os.getenv("TOY_SERVICE_URL", "http://localhost:8001"),
        "trip_service_url": os.getenv("TRIP_SERVICE_URL", "http://localhost:8002"),
    }


@pytest.fixture(scope="session")
def user_oid(auth_token: dict) -> str:
    """Extract user OID from auth token claims."""
    return auth_token["claims"]["oid"]


@pytest.fixture
def cleanup_toys() -> Generator[list[str], None, None]:
    """
    Track created toy IDs for cleanup after tests.
    
    Usage in test:
        def test_create_toy(cleanup_toys, auth_headers):
            response = httpx.post(url, json=data, headers=auth_headers)
            toy_id = response.json()["id"]
            cleanup_toys.append(toy_id)
            # Test continues...
            # Toy will be deleted automatically after test
    """
    toy_ids = []
    yield toy_ids
    
    # Cleanup created toys
    if toy_ids:
        import httpx
        service_url = os.getenv("TOY_SERVICE_URL", "http://localhost:8000")
        
        # Load token for cleanup
        token_path = Path(__file__).parent.parent.parent / "tools" / "identity" / "auth_token.json"
        if token_path.exists():
            with open(token_path) as f:
                token_data = json.load(f)
            headers = {"Authorization": f"Bearer {token_data['token']}"}
            
            for toy_id in toy_ids:
                try:
                    httpx.delete(f"{service_url}/toy/{toy_id}", headers=headers, timeout=10.0)
                except Exception as e:
                    print(f"Warning: Failed to cleanup toy {toy_id}: {e}")


@pytest.fixture(scope="session")
def check_services_available(service_config: dict):
    """
    Check if required services are running.
    
    Skips tests if services are not accessible.
    """
    import httpx
    
    unavailable = []
    for service_name, url in service_config.items():
        try:
            response = httpx.get(f"{url}/health", timeout=5.0)
            if response.status_code != 200:
                unavailable.append(service_name)
        except Exception:
            unavailable.append(service_name)
    
    if unavailable:
        pytest.skip(
            f"Required services not available: {', '.join(unavailable)}. "
            "Ensure services are running locally."
        )


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test requiring real Azure resources"
    )
    config.addinivalue_line(
        "markers",
        "auth: mark test as requiring real authentication"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )
