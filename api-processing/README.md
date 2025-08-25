# PDF Processing API

## Overview
This service processes PDF documents by extracting content and generating AI-powered summaries. The system is designed for scalability, auditability, and forensic compliance.

Previously processed images, now adapted for PDF processing with content extraction and AI summarization capabilities.

## Running the Service

```bash
cd api-processing
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/process
Accepts PDF file uploads and initiates processing.

**Request:**
- Content-Type: `multipart/form-data`
- File parameter: `file` (PDF file)

**Response:**
```json
{
  "id": "uuid",
  "results_url": "https://example.com/processed/uuid",
  "status": "processing"
}
```

## Components Used
- Azure Storage Blob (storing PDF files for long-term forensic access)
- Azure Service Bus (sending processing messages)
- Azure Monitor (monitoring and logging)
- Pydantic (data validation and serialization)
- markitdown (PDF content extraction)

## Features

### PDF Processing
- Accepts PDF file uploads with validation
- Extracts text content using markitdown library
- Generates AI summaries using Azure OpenAI
- Stores results in Cosmos DB with metadata

### Auditing
- Comprehensive audit logging for all operations
- Captures user IP, file metadata, timestamps
- Structured JSON logs for compliance
- Long-term storage retention for forensics
