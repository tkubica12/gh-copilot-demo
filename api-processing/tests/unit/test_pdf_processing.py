"""Unit tests for PDF processing functionality."""

import pytest
import io
import importlib.util
import pathlib
import sys
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


# Import the main module for direct function testing
@pytest.fixture
def api_processing_main():
    """Import the main module to test functions directly."""
    module_key = "api_processing_main"
    if module_key in sys.modules:
        return sys.modules[module_key]
    else:
        module_path = pathlib.Path(__file__).resolve().parents[2] / "main.py"
        spec = importlib.util.spec_from_file_location(module_key, module_path)
        assert spec and spec.loader
        main = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(main)  # type: ignore
        sys.modules[module_key] = main
        return main


def test_validate_file_type_pdf(api_processing_main):
    """Test PDF file type validation."""
    # Create mock PDF file
    mock_file = Mock()
    mock_file.content_type = "application/pdf"
    
    is_valid, file_type = api_processing_main.validate_file_type(mock_file)
    
    assert is_valid is True
    assert file_type == "pdf"


def test_validate_file_type_image(api_processing_main):
    """Test image file type validation."""
    # Create mock image file
    mock_file = Mock()
    mock_file.content_type = "image/jpeg"
    
    is_valid, file_type = api_processing_main.validate_file_type(mock_file)
    
    assert is_valid is True
    assert file_type == "image"


def test_validate_file_type_unsupported(api_processing_main):
    """Test unsupported file type validation."""
    # Create mock unsupported file
    mock_file = Mock()
    mock_file.content_type = "text/plain"
    
    is_valid, file_type = api_processing_main.validate_file_type(mock_file)
    
    assert is_valid is False
    assert file_type == "unsupported"


def test_get_blob_extension_pdf(api_processing_main):
    """Test blob extension for PDF files."""
    extension = api_processing_main.get_blob_extension("pdf")
    assert extension == ".pdf"


def test_get_blob_extension_image(api_processing_main):
    """Test blob extension for image files."""
    extension = api_processing_main.get_blob_extension("image")
    assert extension == ".jpg"


def test_process_pdf_file_endpoint(client):
    """Test PDF file processing endpoint."""
    # Create mock PDF file content
    pdf_content = b"Mock PDF content for testing"
    
    response = client.post(
        "/api/process",
        files={"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    )
    
    assert response.status_code == 202
    response_data = response.json()
    assert "id" in response_data
    assert "results_url" in response_data
    assert response_data["file_type"] == "pdf"


def test_process_unsupported_file_endpoint(client):
    """Test unsupported file processing endpoint."""
    # Create mock text file content
    text_content = b"Mock text content"
    
    response = client.post(
        "/api/process",
        files={"file": ("test.txt", io.BytesIO(text_content), "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]