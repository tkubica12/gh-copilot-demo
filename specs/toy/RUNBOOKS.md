# Service Runbooks

This document contains operational procedures for maintaining the service in production.

## On-Call Quick Reference
-   **Logs**: Azure Portal -> Log Analytics.
-   **Metrics**: Azure Portal -> ACA Metrics.

## Common Incidents
### High Latency
-   **Check**: Cosmos DB RU consumption.
-   **Mitigation**: Scale up Cosmos DB throughput (if manual) or check for hot partitions.

## Maintenance
### Data Cleanup
-   **Script**: `tools/data/clean-toy-profiles.py` (to be updated for no-auth).
