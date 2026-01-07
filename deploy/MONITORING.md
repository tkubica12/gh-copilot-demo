# Monitoring Setup with Prometheus and Grafana

This document describes the Prometheus metrics and Grafana monitoring setup for the microservices.

## Overview

All microservices expose Prometheus metrics at the `/metrics` endpoint:
- **Toy Service**: HTTP request metrics, toy operations (create, update, delete), avatar uploads
- **Trip Service**: HTTP request metrics, trip operations (create, update, delete), photo uploads
- **Demo Data Init Service**: HTTP request metrics, import operations, items imported

## Architecture

- **Azure Monitor Workspace**: Managed Prometheus service for collecting and storing metrics
- **Azure Managed Grafana**: Visualization platform for metrics dashboards
- **Prometheus Scraping**: Configured via Kubernetes pod annotations

## Deployment

### 1. Deploy Infrastructure with Terraform

The Terraform configuration in `mcp/demo_infra/` includes:

```bash
cd mcp/demo_infra
terraform init
terraform plan
terraform apply
```

This creates:
- Azure Monitor Workspace (managed Prometheus)
- Azure Managed Grafana
- Data Collection Endpoint and Rules
- Role assignments for Grafana to read metrics

### 2. Deploy Microservices to Kubernetes

Deploy the services with Prometheus annotations:

```bash
kubectl apply -f deploy/kubernetes/services/toy-service.yaml
kubectl apply -f deploy/kubernetes/services/trip-service.yaml
kubectl apply -f deploy/kubernetes/services/demo-data-init-service.yaml
```

The Kubernetes manifests include annotations for Prometheus scraping:
```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

### 3. Access Grafana

Get the Grafana endpoint URL:

```bash
terraform output grafana_endpoint
```

Navigate to the URL and log in with your Azure credentials.

### 4. View Dashboards

Three pre-configured dashboards are available:
- **Toy Service Metrics**: Toy operations, avatar uploads, request metrics
- **Trip Service Metrics**: Trip operations, photo uploads, request metrics
- **Demo Data Init Service Metrics**: Import operations, items imported, request metrics

## Metrics Exposed

### Common HTTP Metrics (all services)

- `*_http_requests_total`: Total HTTP requests with labels: method, endpoint, status
- `*_http_request_duration_seconds`: HTTP request latency histogram with labels: method, endpoint

### Toy Service Specific Metrics

- `toy_service_toys_registered_total`: Total number of toys registered
- `toy_service_toys_updated_total`: Total number of toys updated
- `toy_service_toys_deleted_total`: Total number of toys deleted
- `toy_service_avatar_uploads_total`: Total number of avatar uploads
- `toy_service_active_toys`: Current number of active toys (gauge)

### Trip Service Specific Metrics

- `trip_service_trips_created_total`: Total number of trips created
- `trip_service_trips_updated_total`: Total number of trips updated
- `trip_service_trips_deleted_total`: Total number of trips deleted
- `trip_service_photos_uploaded_total`: Total number of photos uploaded
- `trip_service_active_trips`: Current number of active trips (gauge)

### Demo Data Init Service Specific Metrics

- `demo_data_init_import_operations_total`: Total import operations with label: status (success/failure)
- `demo_data_init_toys_imported_total`: Total number of toys imported
- `demo_data_init_trips_imported_total`: Total number of trips imported
- `demo_data_init_photos_imported_total`: Total number of photos imported

## Testing Metrics Locally

To test the metrics endpoint locally:

```bash
cd src/services/toy
python3 main.py
```

Then access the metrics:
```bash
curl http://localhost:8000/metrics
```

You should see Prometheus-format metrics output.

## Querying Metrics

Example Prometheus queries:

### Request rate per service
```promql
rate(toy_service_http_requests_total[5m])
```

### 95th percentile request duration
```promql
histogram_quantile(0.95, rate(toy_service_http_request_duration_seconds_bucket[5m]))
```

### Total toys created
```promql
toy_service_toys_registered_total
```

### Import operation success rate
```promql
rate(demo_data_init_import_operations_total{status="success"}[5m])
```

## Troubleshooting

### Metrics not appearing in Grafana

1. Check that pods have the correct annotations:
   ```bash
   kubectl describe pod <pod-name>
   ```

2. Verify the /metrics endpoint is accessible:
   ```bash
   kubectl port-forward pod/<pod-name> 8000:8000
   curl http://localhost:8000/metrics
   ```

3. Check Data Collection Rule association:
   ```bash
   az monitor data-collection rule association list --resource <aks-resource-id>
   ```

### Grafana connection issues

1. Verify role assignment:
   ```bash
   az role assignment list --scope <monitor-workspace-id>
   ```

2. Check Grafana identity permissions
3. Verify Azure Monitor Workspace integration in Grafana settings

## Additional Resources

- [Azure Monitor Workspace documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/azure-monitor-workspace-overview)
- [Azure Managed Grafana documentation](https://learn.microsoft.com/en-us/azure/managed-grafana/)
- [Prometheus Python client documentation](https://prometheus.github.io/client_python/)
