"""Test configuration for worker module."""

import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    test_env = {
        "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=test-key",
        "AZURE_OPENAI_API_KEY": "test-api-key",
        "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
        "SERVICEBUS_FQDN": "test.servicebus.windows.net",
        "SERVICEBUS_QUEUE": "test-queue",
        "STORAGE_ACCOUNT_URL": "https://test.blob.core.windows.net",
        "STORAGE_CONTAINER": "test-container",
        "BATCH_SIZE": "1",
        "BATCH_MAX_WAIT_TIME": "1.0",
        "COSMOS_ACCOUNT_URL": "https://test.documents.azure.com",
        "COSMOS_DB_NAME": "test-db",
        "COSMOS_CONTAINER_NAME": "test-container"
    }
    
    for key, value in test_env.items():
        if key not in os.environ:
            os.environ[key] = value