"""Integration test for status API with real Cosmos DB.

Skips unless RUN_INTEGRATION_TESTS=1 and required environment variables are set
and point to an existing database + container where we can upsert a document.
"""

import os
import uuid
import pytest
from dotenv import load_dotenv
import asyncio
from fastapi.testclient import TestClient
import importlib.util
import pathlib
import sys

# Load .env early so skip condition sees variables
load_dotenv(dotenv_path=pathlib.Path(__file__).resolve().parents[2] / ".env")

required_env_vars = [
    "COSMOS_ACCOUNT_URL",
    "COSMOS_DB_NAME",
    "COSMOS_CONTAINER_NAME",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
    "RETRY_AFTER",
]


def missing_any(vs):  # noqa: D401
    return any(not os.getenv(v) for v in vs)


pytestmark = pytest.mark.integration


@pytest.mark.skipif(missing_any(required_env_vars), reason="Missing required Azure env vars for integration test (evaluated at import time)")
def test_status_endpoint_happy_path():
    module_key = "api_status_main"
    if module_key in sys.modules:
        del sys.modules[module_key]
    # tests/integration/<file> -> parents[2] is service root directory
    module_path = pathlib.Path(__file__).resolve().parents[2] / "main.py"
    spec = importlib.util.spec_from_file_location(module_key, module_path)
    assert spec and spec.loader
    main = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(main)  # type: ignore
    sys.modules[module_key] = main

    client = TestClient(main.app)
    guid = str(uuid.uuid4())

    # Upsert item directly via Cosmos SDK (async)
    from azure.identity.aio import DefaultAzureCredential
    from azure.cosmos.aio import CosmosClient

    async def _upsert():
        cred = DefaultAzureCredential()
        cosmos = CosmosClient(os.environ["COSMOS_ACCOUNT_URL"], credential=cred)
        db = cosmos.get_database_client(os.environ["COSMOS_DB_NAME"])
        container = db.get_container_client(os.environ["COSMOS_CONTAINER_NAME"])
        await container.upsert_item({"id": guid, "ai_response": "ok", "partitionKey": guid})
        await cosmos.close()

    asyncio.get_event_loop().run_until_complete(_upsert())

    r = client.get(f"/api/status/{guid}")
    assert r.status_code == 200
    assert r.json()["data"]["result"] == "ok"
