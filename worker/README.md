# Image and PDF processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI vision capabilities and PDFs using markitdown for text extraction and AI summarization, then stores the results in Azure Cosmos DB.

## File Processing Capabilities
- **Images**: AI-powered image description using Azure OpenAI vision models
- **PDFs**: Text extraction using markitdown library followed by AI summarization

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images and PDFs)
- Azure OpenAI (processing images and generating summaries)
- Azure Cosmos DB (storing results with enhanced audit information)
- MarkItDown (PDF text extraction)

## Auditing and Forensics
- Enhanced audit trails with processing timestamps
- File metadata preservation (original filename, content type, file size)
- Long-term storage in blob storage for forensics requirements
