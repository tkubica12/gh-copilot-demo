# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)
- Prometheus (metrics)

## Metrics

The service exposes Prometheus metrics on port 8000 at the `/metrics` endpoint, including:
- `worker_messages_processed_total`: Total number of successfully processed messages
- `worker_messages_failed_total`: Total number of failed messages
- `worker_message_processing_seconds`: Message processing duration histogram
- `worker_queue_depth`: Current number of messages in the batch
- `worker_openai_api_seconds`: OpenAI API call duration histogram

Set the `PROMETHEUS_PORT` environment variable to change the metrics port (default: 8000).

