"""
Simple test to verify PDF processing functionality works.
"""
import pytest
import sys
import os

# Add the api-processing directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api-processing'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'worker'))

from models.pdf_models import ProcessPdfResponse, PdfProcessingResult, AuditLog
from datetime import datetime


def test_process_pdf_response_model():
    """Test that ProcessPdfResponse model validates correctly."""
    response = ProcessPdfResponse(
        id="test-id",
        results_url="https://example.com/test-id",
        status="processing"
    )
    
    assert response.id == "test-id"
    assert response.results_url == "https://example.com/test-id"
    assert response.status == "processing"


def test_pdf_processing_result_model():
    """Test that PdfProcessingResult model validates correctly."""
    result = PdfProcessingResult(
        id="test-id",
        original_filename="test.pdf",
        content_text="This is test content",
        ai_summary="This is a test summary",
        file_size_bytes=1024,
        page_count=5
    )
    
    assert result.id == "test-id"
    assert result.original_filename == "test.pdf"
    assert result.content_text == "This is test content"
    assert result.ai_summary == "This is a test summary"
    assert result.file_size_bytes == 1024
    assert result.page_count == 5
    assert isinstance(result.processing_timestamp, datetime)


def test_audit_log_model():
    """Test that AuditLog model validates correctly."""
    audit_log = AuditLog(
        operation_id="test-op-id",
        operation_type="upload",
        file_name="test.pdf",
        file_size_bytes=1024,
        status="success"
    )
    
    assert audit_log.operation_id == "test-op-id"
    assert audit_log.operation_type == "upload"
    assert audit_log.file_name == "test.pdf"
    assert audit_log.file_size_bytes == 1024
    assert audit_log.status == "success"
    assert isinstance(audit_log.timestamp, datetime)


if __name__ == "__main__":
    test_process_pdf_response_model()
    test_pdf_processing_result_model()
    test_audit_log_model()
    print("All tests passed!")