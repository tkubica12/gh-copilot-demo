# AI processing worker

This worker listens to messages from an Azure Service Bus queue, processes images and PDFs, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading files)
- Azure OpenAI (processing images and summarizing PDFs)
- Azure Cosmos DB (storing results)
