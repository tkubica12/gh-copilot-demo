# Shared Deployment Strategy

Capture the release workflow and infrastructure expectations that apply across all services in the monorepo.

## Environments
| Environment | Purpose | Infrastructure | Promotion Criteria |
| --- | --- | --- | --- |
| **Local** | Development | Docker Compose / Aspire, Cosmos Emulator, Azurite | Tests pass locally |
| **Dev** | Integration | Azure Container Apps, Cosmos DB (Serverless), Blob Storage | CI pipeline pass |

## CI/CD Pipeline
- **Build**: GitHub Actions builds Docker images and pushes to Azure Container Registry (ACR).
- **Deploy**: GitHub Actions deploys new revisions to Azure Container Apps using Bicep or `az containerapp update`.
- **Verification**: Smoke tests run against the deployed environment.

## Release Patterns
- **Rolling Update**: Standard deployment for ACA. New revision replaces old one.
- **Infrastructure as Code**: Bicep is used to define all Azure resources.

## Approvals & Compliance
- **Code Review**: Required for all PRs.
- **Automated Scans**: Linting and security scans in CI.

## Specification by Example
- **Given** a commit to `main`, **Then** the CI pipeline builds images, pushes to ACR, and updates the ACA revision in the Dev environment.
