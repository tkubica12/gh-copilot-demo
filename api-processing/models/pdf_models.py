"""
Pydantic models for PDF processing data validation and serialization.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProcessPdfRequest(BaseModel):
    """Request model for PDF processing."""
    
    # File will be handled by FastAPI's UploadFile directly
    pass


class ProcessPdfResponse(BaseModel):
    """Response model for PDF processing request."""
    
    id: str = Field(..., description="Unique identifier for the processing job")
    results_url: str = Field(..., description="URL to check processing results")
    status: str = Field(default="processing", description="Current processing status")


class PdfProcessingResult(BaseModel):
    """Model for PDF processing results stored in database."""
    
    id: str = Field(..., description="Unique identifier matching the processing job")
    original_filename: str = Field(..., description="Original PDF filename")
    content_text: str = Field(..., description="Extracted text content from PDF")
    ai_summary: str = Field(..., description="AI-generated summary of the PDF content")
    processing_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When processing completed")
    file_size_bytes: int = Field(..., description="Size of the original PDF file in bytes")
    page_count: Optional[int] = Field(None, description="Number of pages in the PDF")


class AuditLog(BaseModel):
    """Model for audit logging of PDF processing operations."""
    
    operation_id: str = Field(..., description="Unique identifier for the operation")
    operation_type: str = Field(..., description="Type of operation (upload, process, retrieve)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the operation occurred")
    user_ip: Optional[str] = Field(None, description="IP address of the requesting user")
    file_name: str = Field(..., description="Name of the file being processed")
    file_size_bytes: int = Field(..., description="Size of the file in bytes")
    status: str = Field(..., description="Status of the operation (success, error, processing)")
    error_message: Optional[str] = Field(None, description="Error message if operation failed")