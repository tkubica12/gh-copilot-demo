"""
Pydantic models for PDF processing data validation and serialization.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PdfProcessingResult(BaseModel):
    """Model for PDF processing results stored in database."""
    
    id: str = Field(..., description="Unique identifier matching the processing job")
    original_filename: str = Field(..., description="Original PDF filename")
    content_text: str = Field(..., description="Extracted text content from PDF")
    ai_summary: str = Field(..., description="AI-generated summary of the PDF content")
    processing_timestamp: datetime = Field(default_factory=datetime.utcnow, description="When processing completed")
    file_size_bytes: int = Field(..., description="Size of the original PDF file in bytes")
    page_count: Optional[int] = Field(None, description="Number of pages in the PDF")


class ServiceBusMessage(BaseModel):
    """Model for Service Bus message data."""
    
    blob_name: str = Field(..., description="Name of the blob in storage")
    id: str = Field(..., description="Unique identifier for the processing job")
    original_filename: str = Field(..., description="Original filename")
    file_size_bytes: int = Field(..., description="Size of the file in bytes")
    processing_type: str = Field(..., description="Type of processing to perform")