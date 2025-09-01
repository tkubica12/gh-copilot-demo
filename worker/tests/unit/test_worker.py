"""Unit tests for worker service core functions.

These tests mock Azure dependencies and only verify application logic.
"""

import os
import pytest
import json
from unittest.mock import AsyncMock, patch


def test_get_env_var_returns_value_when_set(worker_module):
    """Test get_env_var returns the environment variable value when set."""
    os.environ["TEST_VAR"] = "test_value"
    result = worker_module.get_env_var("TEST_VAR")
    assert result == "test_value"
    # Clean up
    del os.environ["TEST_VAR"]


def test_get_env_var_raises_error_when_not_set(worker_module):
    """Test get_env_var raises EnvironmentError when variable is not set."""
    # Ensure the variable is not set
    if "NONEXISTENT_VAR" in os.environ:
        del os.environ["NONEXISTENT_VAR"]
    
    with pytest.raises(EnvironmentError) as exc_info:
        worker_module.get_env_var("NONEXISTENT_VAR")
    
    assert "NONEXISTENT_VAR environment variable is not set" in str(exc_info.value)


def test_get_env_var_raises_error_when_empty_string(worker_module):
    """Test get_env_var raises EnvironmentError when variable is empty string."""
    os.environ["EMPTY_VAR"] = ""
    
    with pytest.raises(EnvironmentError) as exc_info:
        worker_module.get_env_var("EMPTY_VAR")
    
    assert "EMPTY_VAR environment variable is not set" in str(exc_info.value)
    # Clean up
    del os.environ["EMPTY_VAR"]


@pytest.mark.asyncio
async def test_process_message_success(worker_module):
    """Test process_message successfully processes a message and stores result."""
    # Create mock message
    message_data = {
        "blob_name": "test-image.jpg",
        "id": "test-guid-123"
    }
    mock_message = MockMessage(json.dumps(message_data))
    mock_receiver = AsyncMock()
    
    # Call process_message
    await worker_module.process_message(mock_message, mock_receiver)
    
    # Verify message was completed
    mock_receiver.complete_message.assert_called_once_with(mock_message)
    mock_receiver.abandon_message.assert_not_called()
    
    # Verify cosmos container received the upserted document
    cosmos_container = worker_module._test_cosmos_container
    assert len(cosmos_container.upserted_items) == 1
    upserted_doc = cosmos_container.upserted_items[0]
    assert upserted_doc["id"] == "test-guid-123"
    assert "ai_response" in upserted_doc
    assert upserted_doc["ai_response"] == "This is a fake AI response describing the image."


@pytest.mark.asyncio
async def test_process_message_invalid_json(worker_module):
    """Test process_message handles invalid JSON gracefully."""
    # Create mock message with invalid JSON
    mock_message = MockMessage("invalid-json-data")
    mock_receiver = AsyncMock()
    
    # Call process_message - should handle exception and abandon message
    await worker_module.process_message(mock_message, mock_receiver)
    
    # Verify message was abandoned, not completed
    mock_receiver.abandon_message.assert_called_once_with(mock_message)
    mock_receiver.complete_message.assert_not_called()


@pytest.mark.asyncio 
async def test_process_message_missing_fields(worker_module):
    """Test process_message handles messages with missing required fields."""
    # Create mock message missing required fields
    message_data = {"some_field": "value"}  # Missing blob_name and id
    mock_message = MockMessage(json.dumps(message_data))
    mock_receiver = AsyncMock()
    
    # Call process_message
    await worker_module.process_message(mock_message, mock_receiver)
    
    # Should still complete message even with missing fields (graceful handling)
    # The actual behavior depends on implementation - current code uses .get() with defaults
    mock_receiver.complete_message.assert_called_once_with(mock_message)


@pytest.mark.asyncio
async def test_process_message_openai_exception(worker_module, monkeypatch):
    """Test process_message handles OpenAI API exceptions gracefully."""
    # Mock OpenAI client to raise an exception
    class FailingOpenAIClient:
        def __init__(self, *args, **kwargs):
            self.chat = self
            
        def __getattr__(self, name):
            return self
            
        async def create(self, *args, **kwargs):
            raise Exception("OpenAI API error")
    
    monkeypatch.setattr(worker_module, "client", FailingOpenAIClient())
    
    message_data = {
        "blob_name": "test-image.jpg",
        "id": "test-guid-123"
    }
    mock_message = MockMessage(json.dumps(message_data))
    mock_receiver = AsyncMock()
    
    # Call process_message
    await worker_module.process_message(mock_message, mock_receiver)
    
    # Verify message was abandoned due to exception
    mock_receiver.abandon_message.assert_called_once_with(mock_message)
    mock_receiver.complete_message.assert_not_called()


@pytest.mark.asyncio
async def test_process_message_cosmos_exception(worker_module, monkeypatch):
    """Test process_message handles Cosmos DB exceptions gracefully."""
    # Mock cosmos container to raise an exception
    class FailingCosmosContainer:
        async def upsert_item(self, doc):
            raise Exception("Cosmos DB error")
    
    monkeypatch.setattr(worker_module, "cosmos_container", FailingCosmosContainer())
    
    message_data = {
        "blob_name": "test-image.jpg", 
        "id": "test-guid-123"
    }
    mock_message = MockMessage(json.dumps(message_data))
    mock_receiver = AsyncMock()
    
    # Call process_message
    await worker_module.process_message(mock_message, mock_receiver)
    
    # Verify message was abandoned due to exception
    mock_receiver.abandon_message.assert_called_once_with(mock_message)
    mock_receiver.complete_message.assert_not_called()


class MockMessage:
    """Mock Service Bus message for testing."""
    
    def __init__(self, body_content):
        self.body_content = body_content
    
    def __str__(self):
        return self.body_content