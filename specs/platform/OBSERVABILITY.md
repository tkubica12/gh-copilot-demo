# Shared Observability Strategy

Use this document to capture telemetry standards that apply to every service in the monorepo.

## Instrumentation Baseline
- **Library**: OpenTelemetry (OTEL) Python SDK.
- **Propagation**: W3C Trace Context.
- **Logging**: JSON format with trace/span IDs injected.

## Metrics & SLOs
| Metric | Definition | Target/SLO | Collection Notes |
| --- | --- | --- | --- |
| **Request Latency** | P95 duration of HTTP requests | < 500ms | Auto-instrumented by FastAPI |
| **Error Rate** | % of 5xx responses | < 0.1% | Auto-instrumented |

## Tracing
- **Sampling**: 100% sampling in Dev/Local (for debugging), adaptive sampling in Production (if we had one).
- **Attributes**: `service.name` is mandatory.

## Logging
- **Level**: INFO in production. DEBUG allowed in Local.
- **Sinks**:
    - **Local**: Console / Aspire Dashboard.
    - **Cloud**: Azure Monitor Application Insights (via OTEL Collector).

## Alerting & Dashboards
- **Dashboards**: Azure Monitor Workbooks for cloud, Aspire Dashboard for local.

## Specification by Example
- **Given** a request to `Web` -> `Agent` -> `Toy`, **Then** a single trace ID connects all spans across these services.
