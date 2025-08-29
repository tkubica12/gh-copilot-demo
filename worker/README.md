# AI processing worker

This worker listens to messages from an Azure Service Bus queue, processes images and PDFs using AI, and stores the results in Azure Cosmos DB.

## Processing Capabilities
- **Image Analysis**: Uses Azure OpenAI vision models to describe and analyze images
- **PDF Summarization**: Extracts text from PDFs using markitdown library and generates summaries using Azure OpenAI
- **Auditing**: Comprehensive logging of all processing activities for compliance and forensics

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading files)
- Azure OpenAI (processing images and generating text summaries)
- Azure Cosmos DB (storing results with metadata)
- MarkItDown (PDF text extraction)
- Azure Monitor (distributed tracing and auditing)
