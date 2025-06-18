# API processing

This API accepts image and PDF uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at /api/process

## Supported File Types
- Images (JPEG) - for visual analysis and description
- PDF documents - for text extraction and summarization

## Components Used
- Azure Storage Blob (storing files for long-term access and forensics)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)
