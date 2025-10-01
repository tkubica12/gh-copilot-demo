# Grafana Dashboards

This directory contains Grafana dashboard definitions for monitoring the microservices.

## Dashboards

### API Processing Service (`api-processing.json`)
Monitors the image processing API service with the following panels:
- **Request Rate**: Requests per second over time
- **Total Requests per Second**: Current aggregate request rate
- **Response Time Percentiles**: p50 and p95 latency metrics
- **Error Rate**: Percentage of 5xx responses

### API Status Service (`api-status.json`)
Monitors the status API service with the following panels:
- **Request Rate**: Requests per second over time
- **Total Requests per Second**: Current aggregate request rate
- **Response Time Percentiles**: p50 and p95 latency metrics
- **Response Status Distribution**: Breakdown by status code (200, 202, 5xx)

### Worker Service (`worker.json`)
Monitors the AI worker service with the following panels:
- **Messages Processed Rate**: Rate of successful and failed message processing
- **Current Queue Depth**: Number of messages in the queue
- **Message Processing Time Percentiles**: p50 and p95 processing duration
- **OpenAI API Call Duration Percentiles**: p50 and p95 API call latency
- **Failure Rate**: Percentage of failed message processing
- **Total Messages Processed**: Cumulative count

## Importing Dashboards

### Manual Import
1. Navigate to your Azure Managed Grafana instance
2. Go to **Dashboards** → **Import**
3. Upload the JSON file or paste its contents
4. Configure the Prometheus data source
5. Click **Import**

### Automated Import (via Terraform)
The dashboards can be automatically imported using the Grafana Terraform provider. This is the recommended approach for production environments.

## Metrics

### FastAPI Services (api-processing, api-status)
The FastAPI services expose Prometheus metrics at the `/metrics` endpoint using the `prometheus-fastapi-instrumentator` library. Key metrics include:
- `http_requests_total`: Total HTTP requests by method, path, and status
- `http_request_duration_seconds`: Request duration histogram

### Worker Service
The worker service exposes custom Prometheus metrics on port 8000:
- `worker_messages_processed_total`: Total messages successfully processed
- `worker_messages_failed_total`: Total messages that failed processing
- `worker_message_processing_seconds`: Message processing duration histogram
- `worker_queue_depth`: Current number of messages in the queue
- `worker_openai_api_seconds`: OpenAI API call duration histogram

## Data Source Configuration

These dashboards expect a Prometheus data source configured in Grafana. The data source should point to the Azure Monitor Workspace that scrapes metrics from the Container Apps environment.

## Customization

Feel free to customize these dashboards based on your specific monitoring needs:
- Adjust time ranges and refresh intervals
- Add additional panels for specific metrics
- Create alerts based on thresholds
- Add variables for filtering by instance or other labels
