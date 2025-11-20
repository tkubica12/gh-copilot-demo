# Service Observability Plan

Describe the metrics, logs, and traces that prove this service is healthy. Inherit global goals from `../../platform/OBSERVABILITY.md`.

## Metrics
| Metric | Purpose | Target | Dashboard |
| --- | --- | --- | --- |
| `toy_registered_total` | Count of new toys | N/A | Business |

## Logs
-   **Structured**: JSON.
-   **Attributes**: `toy_id` included in operations.

## Traces
-   **Spans**: `create_toy`, `upload_avatar`.
