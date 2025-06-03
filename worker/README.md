# File processing worker

This worker listens to messages from an Azure Service Bus queue, processes both images and PDF documents using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Processing Capabilities
- **Images**: Uses Azure OpenAI Vision API to generate descriptions
- **PDF Documents**: Extracts text content and generates summaries using Azure OpenAI

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading files)
- Azure OpenAI (processing files - Vision API for images, Chat API for PDFs)
- Azure Cosmos DB (storing results)
- PyPDF2 (PDF text extraction)
