"""Basic tests for worker PDF processing functionality."""

import pytest
from unittest.mock import Mock, patch
import sys
import os
import io

# Set environment variables before importing
os.environ.setdefault("APPLICATIONINSIGHTS_CONNECTION_STRING", "InstrumentationKey=12345678-1234-1234-1234-123456789012")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT_NAME", "test-deployment")
os.environ.setdefault("SERVICEBUS_FQDN", "test.servicebus.windows.net")
os.environ.setdefault("SERVICEBUS_QUEUE", "test-queue")
os.environ.setdefault("STORAGE_ACCOUNT_URL", "https://test.blob.core.windows.net")
os.environ.setdefault("STORAGE_CONTAINER", "test-container")
os.environ.setdefault("BATCH_SIZE", "1")
os.environ.setdefault("BATCH_MAX_WAIT_TIME", "1.0")
os.environ.setdefault("COSMOS_ACCOUNT_URL", "https://test.documents.azure.com")
os.environ.setdefault("COSMOS_DB_NAME", "test-db")
os.environ.setdefault("COSMOS_CONTAINER_NAME", "test-container")

# Add the worker directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import worker functions
from main import is_pdf_file, extract_pdf_content


def test_is_pdf_file():
    """Test PDF file detection."""
    assert is_pdf_file("document.pdf") is True
    assert is_pdf_file("document.PDF") is True
    assert is_pdf_file("image.jpg") is False
    assert is_pdf_file("text.txt") is False


@patch('main.markdown_converter')
def test_extract_pdf_content_success(mock_converter):
    """Test successful PDF content extraction."""
    # Mock the converter result
    mock_result = Mock()
    mock_result.text_content = "Extracted PDF text content"
    mock_result.markdown = "# Extracted PDF content"
    mock_converter.convert.return_value = mock_result
    
    # Test data
    pdf_data = b"Mock PDF binary data"
    
    # Call the function
    result = extract_pdf_content(pdf_data)
    
    # Assertions
    assert result == "Extracted PDF text content"
    mock_converter.convert.assert_called_once()
    
    # Verify BytesIO was used correctly
    call_args = mock_converter.convert.call_args[0][0]
    assert isinstance(call_args, io.BytesIO)


@patch('main.markdown_converter')
def test_extract_pdf_content_fallback_to_markdown(mock_converter):
    """Test PDF content extraction when text_content is None."""
    # Mock the converter result with no text_content
    mock_result = Mock()
    mock_result.text_content = None
    mock_result.markdown = "# Extracted PDF content"
    mock_converter.convert.return_value = mock_result
    
    # Test data
    pdf_data = b"Mock PDF binary data"
    
    # Call the function
    result = extract_pdf_content(pdf_data)
    
    # Should fallback to markdown
    assert result == "# Extracted PDF content"


@patch('main.markdown_converter')
def test_extract_pdf_content_error_handling(mock_converter):
    """Test PDF content extraction error handling."""
    # Mock converter to raise an exception
    mock_converter.convert.side_effect = Exception("PDF parsing failed")
    
    # Test data
    pdf_data = b"Invalid PDF data"
    
    # Call the function and expect an exception
    with pytest.raises(Exception) as exc_info:
        extract_pdf_content(pdf_data)
    
    assert "Failed to extract PDF content" in str(exc_info.value)


# Note: More comprehensive tests would require proper async testing setup
# and mocking of Azure services, which is beyond the scope of this minimal change