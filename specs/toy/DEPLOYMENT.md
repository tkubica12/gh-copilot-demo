# Service Deployment Plan

Describe how this service moves from commit to production, referencing shared workflows in `../../platform/DEPLOYMENT.md`.

## Pipelines
-   **Build**: Docker build `src/services/toy`.
-   **Deploy**: Deploy to ACA app `toy-service`.

## Environments
| Environment | Branch/Artifact | Purpose | Approvals |
| --- | --- | --- | --- |
| **Dev** | `main` | Integration | None |

## Infrastructure
-   **Azure Container App**: `toy-service`
-   **Cosmos Container**: `toys`
-   **Blob Container**: `avatars`
