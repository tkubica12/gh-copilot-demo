"""Common pytest fixtures for api-processing service.

Sets required environment variables before importing the FastAPI app so that
`main.py` can be imported without referencing real Azure resources. Azure
client objects are monkeypatched with simple fakes for unit tests.
"""

import os
import json
import importlib.util
import pathlib
import sys
import pytest
from dotenv import load_dotenv


REQUIRED_ENV = {
    "STORAGE_ACCOUNT_URL": "https://examplestorage.blob.core.windows.net",
    "STORAGE_CONTAINER": "images",
    "PROCESSED_BASE_URL": "https://example.com/processed",
    "SERVICEBUS_FQDN": "example.servicebus.windows.net",
    "SERVICEBUS_QUEUE": "processing",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=00000000-0000-0000-0000-000000000000",
}


@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    """Load .env file then ensure required defaults for unit tests.

    Order:
    1. Load values from service .env (if present)
    2. Backfill any missing required vars with deterministic test defaults
    """
    env_path = pathlib.Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)  # does not override existing process env vars
    for k, v in REQUIRED_ENV.items():
        if not os.environ.get(k):  # only set if still missing
            os.environ[k] = v


@pytest.fixture
def app(monkeypatch, set_env_vars):  # noqa: D401
    """Return FastAPI app with Azure dependencies faked for unit tests."""
    # Dynamically import module because directory name has a hyphen.
    module_key = "api_processing_main"
    if module_key in sys.modules:
        main = sys.modules[module_key]  # type: ignore
    else:
        module_path = pathlib.Path(__file__).resolve().parents[1] / "main.py"
        spec = importlib.util.spec_from_file_location(module_key, module_path)
        assert spec and spec.loader
        main = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(main)  # type: ignore
        sys.modules[module_key] = main

    # Fake storage client
    uploaded = {}

    class FakeContainerClient:
        def upload_blob(self, name, data, overwrite=False):  # noqa: D401
            uploaded[name] = data.read() if hasattr(data, "read") else data

    class FakeQueueSender:
        sent_messages = []

        def send_messages(self, message):  # noqa: D401
            # message has .body (bytes) but in our code we pass ServiceBusMessage(JSON)
            # We will allow anything and store a parsed json when possible.
            body = getattr(message, "body", None)
            if body is None and hasattr(message, "_body" ):
                body = message._body  # type: ignore  # pragma: no cover
            try:
                parsed = json.loads(body) if isinstance(body, (bytes, bytearray)) else json.loads(str(message))
            except Exception:  # pragma: no cover - fall back
                parsed = str(message)
            self.sent_messages.append(parsed)

    monkeypatch.setattr(main, "container_client", FakeContainerClient())
    fake_queue = FakeQueueSender()
    monkeypatch.setattr(main, "servicebus_queue", fake_queue)

    # Expose helpers for assertions
    main._test_uploaded = uploaded  # type: ignore[attr-defined]
    main._test_queue = fake_queue   # type: ignore[attr-defined]
    return main.app


@pytest.fixture
def client(app):  # noqa: D401
    from fastapi.testclient import TestClient

    return TestClient(app)
