# Service Deployment Plan

Describe how this service moves from commit to production, referencing shared workflows in `../../platform/DEPLOYMENT.md`.

## Pipelines
-   **Build**: Docker build `src/services/trip`.
-   **Deploy**: Deploy to ACA app `trip-service`.

## Environments
| Environment | Branch/Artifact | Purpose | Approvals |
| --- | --- | --- | --- |
| **Dev** | `main` | Integration | None |

## Infrastructure
-   **Azure Container App**: `trip-service`
-   **Cosmos Container**: `trips`
-   **Blob Container**: `gallery`
