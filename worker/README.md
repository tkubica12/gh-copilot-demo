# Image processing worker

This worker listens to messages from an Azure Service Bus queue, processes images using Azure OpenAI, and stores the results in Azure Cosmos DB.

## Components Used
- Azure Service Bus (listening to messages)
- Azure Storage Blob (downloading images)
- Azure OpenAI (processing images)
- Azure Cosmos DB (storing results)
- Prometheus (metrics exposure)

## Prometheus Metrics

The worker exposes Prometheus metrics on port 8000 at `/metrics` endpoint.

### Available Metrics
- `worker_messages_processed_total{status}` - Total messages processed (status: success/error)
- `worker_messages_processing_duration_seconds` - Message processing time histogram
- `worker_openai_requests_total{status}` - Total OpenAI API requests (status: success/error)
- `worker_openai_request_duration_seconds` - OpenAI API request duration histogram
- `worker_messages_in_queue` - Current number of messages being processed

### Testing Metrics Locally

The worker starts a Prometheus HTTP server on port 8000 when it runs. To test:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the worker (requires Azure credentials and environment variables)
python main.py
```

In another terminal:
```bash
# Access metrics
curl http://localhost:8000/metrics

# Monitor specific metrics
curl -s http://localhost:8000/metrics | grep worker_messages_processed_total
curl -s http://localhost:8000/metrics | grep worker_openai_requests_total
```

## Running the Worker

Required environment variables:
- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `STORAGE_ACCOUNT_URL`
- `STORAGE_CONTAINER`
- `SERVICEBUS_FQDN`
- `SERVICEBUS_QUEUE`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `COSMOS_ACCOUNT_URL`
- `COSMOS_DB_NAME`
- `COSMOS_CONTAINER_NAME`
- `BATCH_SIZE`
- `BATCH_MAX_WAIT_TIME`

