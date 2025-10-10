"""Integration tests for processing API.

These tests interact with real Azure resources if environment variables and
permissions are provided. They are skipped by default unless RUN_INTEGRATION_TESTS=1.
"""

import os
import io
import json
import time
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import importlib.util
import pathlib
import sys


# Load .env early so skip condition sees variables (fixtures run too late for skipif)
load_dotenv(dotenv_path=pathlib.Path(__file__).resolve().parents[2] / ".env")

required_env_vars = [
    "STORAGE_ACCOUNT_URL",
    "STORAGE_CONTAINER",
    "SERVICEBUS_FQDN",
    "SERVICEBUS_QUEUE",
    "PROCESSED_BASE_URL",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
]


def missing_any(vars_list):  # noqa: D401
    return any(not os.getenv(v) for v in vars_list)


pytestmark = pytest.mark.integration


@pytest.mark.skipif(missing_any(required_env_vars), reason="Missing required Azure env vars for integration test (evaluated at import time)")
def test_end_to_end_blob_and_servicebus():
    # Fresh dynamic import to ensure real Azure clients constructed with current env
    module_key = "api_processing_main"
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
    file_content = b"integration-image-data"
    r = client.post(
        "/api/process",
        files={"file": ("integration.jpg", io.BytesIO(file_content), "image/jpeg")},
    )
    assert r.status_code == 202
    payload = r.json()
    guid = payload["id"]

    # Verify blob exists
    from azure.storage.blob import BlobClient

    blob_client = BlobClient(account_url=os.environ["STORAGE_ACCOUNT_URL"], container_name=os.environ["STORAGE_CONTAINER"], blob_name=f"{guid}.jpg")
    # Existence check by attempting to download a small range
    stream = blob_client.download_blob(offset=0, length=10)
    assert stream.readall()  # have some bytes

    # Verify Service Bus message present (peek / receive)
    from azure.identity import DefaultAzureCredential
    from azure.servicebus import ServiceBusClient

    found = False
    credential = DefaultAzureCredential()
    with ServiceBusClient(os.environ["SERVICEBUS_FQDN"], credential=credential) as sb_client:
        with sb_client.get_queue_receiver(queue_name=os.environ["SERVICEBUS_QUEUE"], max_wait_time=10) as receiver:
            start = time.time()
            while time.time() - start < 15 and not found:
                for msg in receiver.receive_messages(max_message_count=5, max_wait_time=5):
                    try:
                        body = json.loads(str(bytes(msg)))
                    except Exception:  # pragma: no cover - fallback
                        body = {}
                    if body.get("id") == guid:
                        found = True
                    receiver.complete_message(msg)
                if not found:
                    time.sleep(1)
    assert found, "Did not locate Service Bus message for uploaded image"
