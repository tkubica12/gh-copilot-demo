# Prometheus and Grafana Monitoring Setup

This document describes the Prometheus and Grafana monitoring setup for the microservices architecture.

## Architecture

The monitoring solution consists of:

1. **Prometheus Metrics Exporters** in each microservice
2. **Azure Monitor Workspace** (Managed Prometheus) for metric collection
3. **Azure Managed Grafana** for visualization
4. **Data Collection Rules** to scrape metrics from Container Apps

## Microservices Metrics

### API Processing Service

**Endpoint:** `https://<api-processing-url>/metrics`

**Metrics:**
- `http_requests_total` - Total HTTP requests by method, handler, and status
- `http_request_duration_seconds` - HTTP request duration histogram
- `http_request_size_bytes` - HTTP request size
- `http_response_size_bytes` - HTTP response size
- `http_requests_in_progress` - Current number of requests being processed

### API Status Service

**Endpoint:** `https://<api-status-url>/metrics`

**Metrics:**
- `http_requests_total` - Total HTTP requests by method, handler, and status
- `http_request_duration_seconds` - HTTP request duration histogram
- `http_request_size_bytes` - HTTP request size
- `http_response_size_bytes` - HTTP response size
- `http_requests_in_progress` - Current number of requests being processed

### Worker Service

**Endpoint:** `http://<worker-internal>:8000/metrics`

**Metrics:**
- `worker_messages_processed_total{status}` - Total messages processed (status: success/error)
- `worker_messages_processing_duration_seconds` - Message processing time histogram
- `worker_openai_requests_total{status}` - Total OpenAI API requests (status: success/error)
- `worker_openai_request_duration_seconds` - OpenAI API request duration histogram
- `worker_messages_in_queue` - Current number of messages being processed

## Deployment

### 1. Deploy Infrastructure

Deploy the Terraform configuration which includes the Prometheus and Grafana resources:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This creates:
- Azure Monitor Workspace
- Azure Managed Grafana
- Data Collection Endpoint
- Data Collection Rule for Prometheus metrics
- RBAC assignments

**Note:** For the worker service metrics to be scraped, you may need to configure the Container App to expose port 8000 internally for Prometheus scraping. This can be done by adding service configuration in the Container App Environment. The API services automatically expose their `/metrics` endpoint on their existing HTTP port (80).

### 2. Configure Container Apps

The Container Apps are already configured to expose metrics endpoints. The Data Collection Rule automatically scrapes:
- `/metrics` endpoint from API services (ports 80)
- `:8000/metrics` endpoint from Worker service (port 8000)

### 3. Import Grafana Dashboards

After deployment:

1. Get the Grafana URL from Terraform output or Azure Portal
2. Navigate to your Grafana instance
3. Go to **Dashboards** → **Import**
4. Import each dashboard from `grafana-dashboards/`:
   - `api-processing-dashboard.json`
   - `api-status-dashboard.json`
   - `worker-dashboard.json`

### 4. Verify Data Collection

1. Navigate to your Grafana instance
2. Go to **Explore**
3. Select the Azure Monitor Workspace data source
4. Run a test query:
   ```promql
   http_requests_total
   ```

## Testing Metrics Locally

### Test API Services

Start the API service locally:

```bash
cd api-processing  # or api-status
uv sync
uv run uvicorn main:app --port 8080
```

Then access the metrics endpoint:

```bash
curl http://localhost:8080/metrics
```

### Test Worker Service

The worker service exposes metrics on port 8000. Start the service and check:

```bash
curl http://localhost:8000/metrics
```

## Useful Queries

### Request Rate
```promql
rate(http_requests_total[5m])
```

### Request Duration (p95)
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Error Rate
```promql
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
```

### Worker Processing Rate
```promql
rate(worker_messages_processed_total[5m])
```

### Worker Error Rate
```promql
rate(worker_messages_processed_total{status="error"}[5m]) / rate(worker_messages_processed_total[5m])
```

## Alerting (Future Enhancement)

To add alerting:

1. Create alert rules in Grafana
2. Configure notification channels (email, Slack, etc.)
3. Define thresholds for critical metrics:
   - High error rate (>5%)
   - Slow response time (p95 > 2s)
   - High queue depth (>100 messages)

## Troubleshooting

### Metrics Not Appearing

1. Check Container Apps are running:
   ```bash
   az containerapp list --resource-group <rg-name>
   ```

2. Check Data Collection Rule is associated:
   ```bash
   az monitor data-collection rule show --name dcr-prometheus-<base-name> --resource-group <rg-name>
   ```

3. Verify metrics endpoint is accessible from Container App:
   ```bash
   az containerapp exec --name ca-api-processing-<base-name> --resource-group <rg-name> --command "curl localhost:80/metrics"
   ```

### Dashboard Not Loading

1. Verify Grafana has access to the Monitor Workspace
2. Check RBAC assignment for Grafana managed identity
3. Verify the Prometheus data source is configured correctly

## Cost Optimization

- Azure Monitor Workspace charges for data ingestion and queries
- Grafana charges for Standard tier
- To reduce costs:
  - Adjust scrape intervals
  - Filter metrics to only essential ones
  - Use retention policies

## References

- [Azure Monitor Workspace Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/prometheus-metrics-overview)
- [Azure Managed Grafana Documentation](https://learn.microsoft.com/en-us/azure/managed-grafana/overview)
- [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
