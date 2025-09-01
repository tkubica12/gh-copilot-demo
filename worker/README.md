# AI Processing Worker

This worker listens to messages from an Azure Service Bus queue, processes both images and PDFs using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Processing Capabilities

### Image Processing
- Downloads images from Azure Blob Storage
- Uses Azure OpenAI Vision API to generate detailed descriptions
- Processes common image formats (JPEG, PNG, GIF, BMP)

### PDF Processing  
- Downloads PDFs from Azure Blob Storage
- Extracts content using markitdown library
- Generates AI-powered summaries using Azure OpenAI text completion
- Handles text extraction and content analysis

## Components Used
- Azure Service Bus (listening to processing messages)
- Azure Storage Blob (downloading images and PDFs)
- Azure OpenAI (AI processing for both images and documents)
- Azure Cosmos DB (storing processing results)
- markitdown library (PDF content extraction)
- Azure Monitor (audit logging and monitoring)

## Features
- Asynchronous batch processing
- Comprehensive audit logging
- Error handling with message retry
- Support for multiple file types
- Long-term storage for forensic purposes
