# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)
