# Service Observability Plan

Describe the metrics, logs, and traces that prove this service is healthy. Inherit global goals from `../../platform/OBSERVABILITY.md`.

## Metrics
| Metric | Purpose | Target | Dashboard |
| --- | --- | --- | --- |
| `trip_created_total` | Count of new trips | N/A | Business |

## Logs
-   **Structured**: JSON.
-   **Attributes**: `trip_id`, `toy_id`.

## Traces
-   **Spans**: `create_trip`, `upload_gallery_image`.
