# PDF Processing Worker

## Overview
This worker service processes PDF documents by extracting text content and generating AI-powered summaries using Azure OpenAI. It consumes messages from Azure Service Bus and stores results in Cosmos DB.

Previously processed images for AI analysis, now adapted for PDF content extraction and summarization.

## Running the Service

```bash
cd worker
pip install -r requirements.txt
python main.py
```

## Components Used
- Azure Service Bus (receiving processing messages)
- Azure Storage Blob (downloading PDF files)
- Azure Cosmos DB (storing processing results)
- Azure OpenAI (generating summaries)
- Azure Monitor (monitoring and logging)
- markitdown (PDF content extraction)

## Processing Flow

1. **Message Reception**: Receives PDF processing messages from Service Bus
2. **PDF Download**: Downloads PDF files from Azure Blob Storage
3. **Content Extraction**: Uses markitdown to extract text from PDF
4. **AI Summarization**: Generates summary using Azure OpenAI
5. **Result Storage**: Stores extracted content and summary in Cosmos DB
6. **Message Completion**: Marks Service Bus message as completed

## Features

### PDF Content Extraction
- Robust PDF-to-text conversion using markitdown
- Handles various PDF formats and encodings
- Page count estimation from content structure

### AI Summarization
- Azure OpenAI integration for document summarization
- Optimized prompts for concise, informative summaries
- Configurable temperature and token limits

### Error Handling
- Graceful error handling with message abandonment
- Detailed error logging with operation context
- Automatic retry via Service Bus dead letter handling

## Data Storage
Results are stored in Cosmos DB with the following structure:
```json
{
  "id": "unique-identifier",
  "original_filename": "document.pdf",
  "content_text": "extracted text content",
  "ai_summary": "AI-generated summary",
  "processing_timestamp": "2024-01-01T00:00:00Z",
  "file_size_bytes": 1024,
  "page_count": 5
}
```
