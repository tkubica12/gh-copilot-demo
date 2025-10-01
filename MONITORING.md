# Monitoring and Observability

This document describes the monitoring setup for the microservices in this project.

## Overview

The application uses a multi-layered observability approach:

1. **Application Insights** - Distributed tracing and application performance monitoring
2. **Prometheus Metrics** - Time-series metrics for monitoring service health and performance
3. **Azure Monitor Workspace** - Managed Prometheus service for metrics collection
4. **Azure Managed Grafana** - Visualization and dashboarding

## Architecture

```
┌─────────────────────┐
│  Microservices      │
│  - api-processing   │──┐
│  - api-status       │  │ /metrics endpoints
│  - worker           │  │
└─────────────────────┘  │
                         │
                         ▼
┌──────────────────────────────────────┐
│  Container Apps Environment          │
│  (OpenTelemetry Configuration)       │
└──────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────┐
│  Azure Monitor Workspace             │
│  (Managed Prometheus)                │
└──────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────┐
│  Azure Managed Grafana               │
│  - Pre-built Dashboards              │
└──────────────────────────────────────┘
```

## Metrics Exposed

### API Services (api-processing, api-status)

Both FastAPI services expose Prometheus metrics at `GET /metrics`:

- `http_requests_total` - Total HTTP requests by method, path, and status code
- `http_request_duration_seconds` - Request duration histogram with buckets
- `http_requests_in_progress` - Number of requests currently being processed

### Worker Service

The worker service exposes custom metrics on port 8000 at `/metrics`:

- `worker_messages_processed_total` - Counter of successfully processed messages
- `worker_messages_failed_total` - Counter of failed messages
- `worker_message_processing_seconds` - Histogram of message processing duration
- `worker_queue_depth` - Gauge showing current batch size
- `worker_openai_api_seconds` - Histogram of OpenAI API call duration

## Infrastructure Components

### Azure Monitor Workspace

Created via Terraform as `azurerm_monitor_workspace.main`. This is a managed Prometheus-compatible service that:
- Collects metrics from Container Apps
- Provides PromQL query interface
- Integrates with Grafana

### Azure Managed Grafana

Created via Terraform as `azurerm_dashboard_grafana.main`. Features:
- Pre-configured integration with Azure Monitor Workspace
- System-assigned managed identity
- Standard SKU for production use

### Container Apps Environment Configuration

The Container Apps environment is configured with OpenTelemetry to send metrics to Azure Monitor Workspace:
- Metrics destination: Azure Monitor Workspace
- Transport: OTLP (OpenTelemetry Protocol)
- Configuration managed via `azapi_update_resource`

## Grafana Dashboards

Pre-built dashboards are available in the `grafana-dashboards/` directory:

### API Processing Dashboard
File: `api-processing.json`

Panels:
- Request rate over time
- Total requests per second
- Response time percentiles (p50, p95)
- Error rate (5xx responses)

### API Status Dashboard
File: `api-status.json`

Panels:
- Request rate over time
- Total requests per second
- Response time percentiles (p50, p95)
- Response status distribution (200, 202, 5xx)

### Worker Dashboard
File: `worker.json`

Panels:
- Messages processed rate (success/failure)
- Current queue depth
- Message processing time percentiles
- OpenAI API call duration percentiles
- Failure rate percentage
- Total messages processed counter

## Accessing Monitoring

### Grafana UI
1. Navigate to the Azure Portal
2. Find the Managed Grafana resource (name: `grafana-{prefix}`)
3. Click "Endpoint" to access the Grafana UI
4. Import dashboards from `grafana-dashboards/` directory

### Prometheus Queries
You can query metrics directly using PromQL in Grafana's Explore view. Example queries:

```promql
# Request rate for api-processing
rate(http_requests_total{job="api-processing"}[5m])

# p95 response time for api-status
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="api-status"}[5m]))

# Worker failure rate
rate(worker_messages_failed_total[5m]) / 
  (rate(worker_messages_processed_total[5m]) + rate(worker_messages_failed_total[5m]))

# Current queue depth
worker_queue_depth
```

## Local Development

To test metrics locally:

1. Start the service (e.g., `uvicorn main:app --host 0.0.0.0 --port 80`)
2. Access metrics endpoint:
   - API services: `http://localhost:80/metrics`
   - Worker: `http://localhost:8000/metrics`
3. Verify Prometheus format output

## Alerting

Consider setting up alerts for:
- High error rates (>5% 5xx responses)
- High response times (p95 > threshold)
- Queue depth buildup (worker_queue_depth > threshold)
- Worker failure rate (>10%)
- Low throughput (messages_processed_total rate drops)

Alerts can be configured in Grafana or Azure Monitor.

## Troubleshooting

### Metrics not appearing in Grafana
1. Verify Container Apps are running and healthy
2. Check that `/metrics` endpoints are accessible
3. Verify OpenTelemetry configuration in Container Apps environment
4. Check Azure Monitor Workspace is properly connected to Grafana

### Missing worker metrics
1. Ensure worker container has ingress configured for port 8000
2. Verify `PROMETHEUS_PORT` environment variable is set correctly
3. Check worker logs for Prometheus startup messages

### Dashboard import issues
1. Ensure Prometheus data source is configured in Grafana
2. Verify data source points to Azure Monitor Workspace
3. Check dashboard JSON syntax is valid

## Best Practices

1. **Regular Dashboard Review** - Review dashboards weekly to understand baseline behavior
2. **Alert Tuning** - Start with conservative thresholds and adjust based on observed patterns
3. **Metrics Cardinality** - Be mindful of label cardinality to avoid performance issues
4. **Dashboard Organization** - Use folders in Grafana to organize dashboards by team/service
5. **Documentation** - Keep dashboard descriptions up-to-date with changes

## References

- [Azure Monitor Workspace Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/azure-monitor-workspace-overview)
- [Azure Managed Grafana Documentation](https://learn.microsoft.com/en-us/azure/managed-grafana/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Container Apps Observability](https://learn.microsoft.com/en-us/azure/container-apps/observability)
