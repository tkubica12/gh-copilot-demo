# Service Runbooks

This document contains operational procedures for maintaining the service in production.

## On-Call Quick Reference
-   **Logs**: Azure Portal -> Log Analytics.
-   **Metrics**: Azure Portal -> ACA Metrics.

## Common Incidents
### High Latency
-   **Check**: Cosmos DB RU consumption.

## Maintenance
### Data Cleanup
-   **Script**: `tools/data/clean-trip-profiles.py` (to be updated).
