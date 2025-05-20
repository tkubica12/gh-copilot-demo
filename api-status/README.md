# API status

This API provides the status and results of processed images stored in Azure Cosmos DB.

## Components Used
- Azure Cosmos DB (reading results)
- Azure Monitor (monitoring and logging)
- Prometheus (performance metrics)

## Monitoring
The service exposes Prometheus metrics at the `/metrics` endpoint for monitoring performance:
- Request latency
- Requests in progress
- Found vs. pending results
- Error counts
- Processing times
