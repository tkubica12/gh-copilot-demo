# API processing

This API accepts image and PDF uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at /api/process

## Components Used
- Azure Storage Blob (storing files)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)

## Supported File Types
- Images (JPG, JPEG, PNG)
- PDF documents
