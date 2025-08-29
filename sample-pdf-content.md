# Sample PDF Content for Testing

This file simulates what would be extracted from a PDF document by the markitdown library.

## Document Title: Technical Specification

### Key Points:
- The system processes both images and PDF documents
- PDFs are analyzed for text content and summarized using AI
- All processing activities are logged for audit purposes
- Files are stored long-term in Azure Blob Storage for forensics
- The solution integrates with Azure OpenAI for intelligent summarization

### Implementation Details:
The PDF processing workflow:
1. Upload PDF via /api/process endpoint  
2. File stored in Azure Blob Storage with forensic retention
3. Message queued in Service Bus for processing
4. Worker extracts text using markitdown library
5. Text summarized using Azure OpenAI
6. Results stored in Cosmos DB with audit metadata

This concludes the sample document content.