# API processing

This API accepts image and PDF file uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at /api/process

## Supported File Types
- Images (JPEG, PNG, etc.) - processed for description using Azure OpenAI Vision API
- PDF documents - processed for text extraction and summarization using Azure OpenAI

## Components Used
- Azure Storage Blob (storing files)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)
