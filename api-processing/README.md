# API processing

This API accepts image and PDF uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at /api/process

## Supported File Types
- JPEG Images (.jpg) - for image description using AI vision
- PDF Documents (.pdf) - for text extraction and summarization using AI

## Components Used
- Azure Storage Blob (storing images and PDFs)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)

## Features
- **File Processing**: Supports both image analysis and PDF summarization
- **Auditing**: Enhanced audit trails for forensics requirements
- **Long-term Storage**: Files are stored in Azure Blob Storage for future forensics needs
