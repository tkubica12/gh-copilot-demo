# API processing

This API accepts image uploads, stores them in Azure Blob Storage, and sends a message to Azure Service Bus for processing.

You can access it at /api/process

## Components Used
- Azure Storage Blob (storing images)
- Azure Service Bus (sending messages)
- Azure Monitor (monitoring and logging)
- Prometheus (performance metrics)

## Monitoring
The service exposes Prometheus metrics at the `/metrics` endpoint for monitoring performance:
- Request latency
- Requests in progress
- Total blob uploads
- Total messages sent
- Upload sizes
- Processing times
