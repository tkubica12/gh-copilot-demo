"""Common pytest fixtures for api-status service.

Provides environment variables and fakes for Cosmos DB for unit tests.
"""

import os
import pytest
import importlib.util
import pathlib
import sys
from dotenv import load_dotenv


REQUIRED_ENV = {
    "COSMOS_ACCOUNT_URL": "https://example-cosmos.documents.azure.com:443/",
    "COSMOS_DB_NAME": "demo-db",
    "COSMOS_CONTAINER_NAME": "results",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=00000000-0000-0000-0000-000000000000",
    "RETRY_AFTER": "5",
}


@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    """Load .env then supply any missing required defaults for unit tests."""
    env_path = pathlib.Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    for k, v in REQUIRED_ENV.items():
        if not os.environ.get(k):
            os.environ[k] = v


@pytest.fixture
def app(monkeypatch, set_env_vars):  # noqa: D401
    module_key = "api_status_main"
    if module_key in sys.modules:
        main = sys.modules[module_key]  # type: ignore
    else:
        module_path = pathlib.Path(__file__).resolve().parents[1] / "main.py"
        spec = importlib.util.spec_from_file_location(module_key, module_path)
        assert spec and spec.loader
        main = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(main)  # type: ignore
        sys.modules[module_key] = main

    class FakeContainer:
        def __init__(self, items):
            self._items = items

        def query_items(self, query, parameters, partition_key):  # noqa: D401
            # Return async iterator over items
            async def iterator():
                for it in self._items:
                    yield it
            return iterator()

    # Inject two variants via attributes for tests to override
    monkeypatch.setattr(main, "container", FakeContainer([]))
    return main.app


@pytest.fixture
def client(app):  # noqa: D401
    from fastapi.testclient import TestClient
    return TestClient(app)
