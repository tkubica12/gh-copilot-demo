"""Integration test for PDF processing message format."""

import io
import sys
from fastapi.testclient import TestClient
import pytest


def test_pdf_processing_message_format(client):
    """Test that PDF processing creates the correct Service Bus message format."""
    # Create mock PDF file
    pdf_content = b"Mock PDF content for integration testing"
    
    response = client.post(
        "/api/process",
        files={"file": ("test_document.pdf", io.BytesIO(pdf_content), "application/pdf")}
    )
    
    assert response.status_code == 202
    response_data = response.json()
    
    # Verify response format
    assert "id" in response_data
    assert "results_url" in response_data
    assert response_data["file_type"] == "pdf"
    
    # Get the test helpers from the main module
    main = sys.modules["api_processing_main"]
    uploaded_files = main._test_uploaded  # type: ignore[attr-defined]
    queue_helper = main._test_queue  # type: ignore[attr-defined]
    
    # Verify file was uploaded to blob storage
    assert len(uploaded_files) >= 1
    # Find the PDF blob
    pdf_blobs = [name for name in uploaded_files.keys() if name.endswith(".pdf")]
    assert len(pdf_blobs) == 1
    blob_name = pdf_blobs[0]
    assert uploaded_files[blob_name] == pdf_content
    
    # Verify message was sent to Service Bus (should be the last message)
    assert len(queue_helper.sent_messages) >= 1
    message = queue_helper.sent_messages[-1]  # Get the last message
    
    # Verify message format
    expected_fields = ["blob_name", "id", "file_type", "original_filename", "timestamp"]
    for field in expected_fields:
        assert field in message, f"Missing field: {field}"
    
    assert message["blob_name"] == blob_name
    assert message["id"] == response_data["id"]
    assert message["file_type"] == "pdf"
    assert message["original_filename"] == "test_document.pdf"
    assert message["timestamp"]  # Should be present and non-empty
    
    print(f"✅ PDF processing message format validated:")
    print(f"   Blob name: {message['blob_name']}")
    print(f"   File type: {message['file_type']}")
    print(f"   Original filename: {message['original_filename']}")


def test_image_processing_still_works(client):
    """Test that existing image processing still works after PDF changes."""
    # Create mock image file
    image_content = b"Mock JPEG image content"
    
    response = client.post(
        "/api/process",
        files={"file": ("test_image.jpg", io.BytesIO(image_content), "image/jpeg")}
    )
    
    assert response.status_code == 202
    response_data = response.json()
    
    # Verify response format
    assert "id" in response_data
    assert "results_url" in response_data
    assert response_data["file_type"] == "image"
    
    # Get the test helpers
    main = sys.modules["api_processing_main"]
    queue_helper = main._test_queue  # type: ignore[attr-defined]
    
    # Verify message format (should be the last message)
    message = queue_helper.sent_messages[-1]
    assert message["file_type"] == "image"
    assert message["original_filename"] == "test_image.jpg"
    
    print(f"✅ Image processing backward compatibility verified")