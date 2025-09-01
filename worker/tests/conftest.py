"""Common pytest fixtures for worker service.

Provides environment variables and fakes for Azure services for unit tests.
"""

import os
import pytest
import importlib.util
import pathlib
import sys
from dotenv import load_dotenv


REQUIRED_ENV = {
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=00000000-0000-0000-0000-000000000000",
    "AZURE_OPENAI_API_KEY": "fake-api-key",
    "AZURE_OPENAI_ENDPOINT": "https://fake-openai.openai.azure.com",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "fake-deployment",
    "SERVICEBUS_FQDN": "fake-servicebus.servicebus.windows.net",
    "SERVICEBUS_QUEUE": "fake-queue",
    "STORAGE_ACCOUNT_URL": "https://fakestorage.blob.core.windows.net/",
    "STORAGE_CONTAINER": "fake-container",
    "BATCH_SIZE": "5",
    "BATCH_MAX_WAIT_TIME": "10.0",
    "COSMOS_ACCOUNT_URL": "https://fake-cosmos.documents.azure.com:443/",
    "COSMOS_DB_NAME": "fake-db",
    "COSMOS_CONTAINER_NAME": "fake-container",
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
def worker_module(monkeypatch, set_env_vars):
    """Return worker main module with Azure dependencies faked for unit tests."""
    # Import main module - need to handle it being run as script
    module_key = "worker_main"
    if module_key in sys.modules:
        main = sys.modules[module_key]
    else:
        module_path = pathlib.Path(__file__).resolve().parents[1] / "main.py"
        spec = importlib.util.spec_from_file_location(module_key, module_path)
        assert spec and spec.loader
        main = importlib.util.module_from_spec(spec)
        
        # Patch module-level imports to prevent actual Azure client creation
        class FakeCredential:
            pass
            
        class FakeServiceBusClient:
            def __init__(self, *args, **kwargs):
                pass
            
            def get_queue_receiver(self, *args, **kwargs):
                return FakeQueueReceiver()
                
            async def __aenter__(self):
                return self
                
            async def __aexit__(self, *args):
                pass
        
        class FakeQueueReceiver:
            async def receive_messages(self, max_message_count=1, max_wait_time=1):
                return []
                
            async def complete_message(self, message):
                pass
                
            async def abandon_message(self, message):
                pass
                
            async def __aenter__(self):
                return self
                
            async def __aexit__(self, *args):
                pass
        
        class FakeBlobServiceClient:
            def __init__(self, *args, **kwargs):
                pass
                
            def get_blob_client(self, container, blob_name):
                return FakeBlobClient(blob_name)
        
        class FakeBlobClient:
            def __init__(self, blob_name):
                self.blob_name = blob_name
                
            async def download_blob(self):
                return FakeBlobDownloadStream()
        
        class FakeBlobDownloadStream:
            async def readall(self):
                return b"fake-image-data"
        
        class FakeCosmosClient:
            def __init__(self, *args, **kwargs):
                pass
                
            def get_database_client(self, db_name):
                return FakeCosmosDatabase()
        
        class FakeCosmosDatabase:
            def get_container_client(self, container_name):
                return FakeCosmosContainer()
        
        class FakeCosmosContainer:
            def __init__(self):
                self.upserted_items = []
                
            async def upsert_item(self, doc):
                self.upserted_items.append(doc)
        
        class FakeOpenAIClient:
            def __init__(self, *args, **kwargs):
                self.chat = FakeChat()
        
        class FakeChat:
            def __init__(self):
                self.completions = FakeChatCompletions()
        
        class FakeChatCompletions:
            async def create(self, *args, **kwargs):
                return FakeOpenAIResponse()
        
        class FakeOpenAIResponse:
            def __init__(self):
                self.choices = [FakeChoice()]
        
        class FakeChoice:
            def __init__(self):
                self.message = FakeMessage()
        
        class FakeMessage:
            def __init__(self):
                self.content = "This is a fake AI response describing the image."
        
        # Mock the module-level Azure clients
        monkeypatch.setattr("azure.identity.aio.DefaultAzureCredential", FakeCredential)
        monkeypatch.setattr("azure.servicebus.aio.ServiceBusClient", FakeServiceBusClient)
        monkeypatch.setattr("azure.storage.blob.aio.BlobServiceClient", FakeBlobServiceClient)
        monkeypatch.setattr("azure.cosmos.aio.CosmosClient", FakeCosmosClient)
        monkeypatch.setattr("openai.AsyncAzureOpenAI", FakeOpenAIClient)
        
        # Mock telemetry configuration to avoid actual setup
        monkeypatch.setattr("azure.monitor.opentelemetry.configure_azure_monitor", lambda *args, **kwargs: None)
        monkeypatch.setattr("opentelemetry.instrumentation.openai_v2.OpenAIInstrumentor", lambda: FakeInstrumentor())
        
        class FakeInstrumentor:
            def instrument(self):
                pass
        
        # Now load the module
        spec.loader.exec_module(main)
        sys.modules[module_key] = main
    
    # Store references to fake services for test assertions
    main._test_cosmos_container = main.cosmos_container
    
    return main