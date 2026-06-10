# Terraform Infrastructure - Demo Application

This Terraform project deploys a complete demo application infrastructure on Azure, showcasing a microservices architecture with Azure Container Apps, Service Bus, Cosmos DB, and Azure Storage.

## Project Overview

This infrastructure is designed to demonstrate GitHub Copilot features and is optimized for learning purposes. It deploys a document processing application with frontend, API services, and background workers.

## Architecture

The infrastructure deploys the following components:

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│  Frontend   │─────▶│  API Processing  │─────▶│ Service Bus │
│ Container   │      │   Container      │      │    Queue    │
└─────────────┘      └──────────────────┘      └─────────────┘
                              │                        │
                              │                        ▼
                              │                 ┌─────────────┐
                              │                 │   Worker    │
                              │                 │  Container  │
                              ▼                 └─────────────┘
                     ┌─────────────┐                   │
                     │   Blob      │                   │
                     │  Storage    │                   ▼
                     └─────────────┘            ┌─────────────┐
                              ▲                 │  Cosmos DB  │
                              │                 └─────────────┘
                     ┌─────────────┐
                     │ API Status  │
                     │  Container  │
                     └─────────────┘
```

## Azure Resources

### Container Apps
- **Frontend** (`container_app.frontend.tf`): Web UI serving the application frontend
- **API Processing** (`container_app.api-processing.tf`): REST API for document upload and processing requests
- **API Status** (`container_app.api-status.tf`): REST API for checking processing status
- **Worker** (`container_app.worker.tf`): Background worker processing documents from Service Bus queue with Azure OpenAI integration
- **Perftest Job** (`container_app_job.perftest.tf`): Performance testing job for load testing

### Data & Messaging Services
- **Azure Cosmos DB** (`cosmos.tf`): NoSQL database for storing processed document data
  - Account with serverless tier
  - SQL database `mydb`
  - Container `mydocuments` with partition key `/id`
  
- **Azure Service Bus** (`service_bus.tf`): Message queue for asynchronous document processing
  - Standard tier namespace
  - Queue `documents-to-process` with partitioning enabled
  
- **Azure Storage Account** (`storage.tf`): Blob storage for document files
  - Standard LRS tier
  - Container `data` for file storage
  - OAuth authentication enabled

### Monitoring & Observability
- **Log Analytics Workspace** (`monitoring.tf`): Centralized logging
- **Application Insights** (`monitoring.tf`): Application performance monitoring and telemetry

### Security & Identity
- **User Assigned Managed Identity** (`identity.tf`): Managed identity for all container apps
- **RBAC Assignments** (`rbac.tf`): Role-based access control for:
  - Storage Blob Data access
  - Service Bus Data Sender/Receiver
  - Cosmos DB SQL access with custom role

### Supporting Resources
- **Container App Environment** (`container_app_env.tf`): Shared environment for all container apps
- **Resource Group** (`main.tf`): Resource group container
- **Random String** (`main.tf`): Random suffix for unique resource naming

## Project Structure

```
.
├── main.tf                           # Resource group and base resources
├── providers.tf                      # Terraform and provider configuration
├── variables.tf                      # Input variables
├── locals.tf                         # Local values for naming
├── identity.tf                       # Managed identity
├── rbac.tf                          # Role assignments
├── container_app_env.tf             # Container Apps environment
├── container_app.frontend.tf        # Frontend container app
├── container_app.api-processing.tf  # API processing container app
├── container_app.api-status.tf      # API status container app
├── container_app.worker.tf          # Worker container app
├── container_app_job.perftest.tf    # Performance test job
├── storage.tf                       # Azure Storage Account
├── service_bus.tf                   # Azure Service Bus
├── cosmos.tf                        # Azure Cosmos DB
└── monitoring.tf                    # Log Analytics and App Insights
```

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed and authenticated
- Azure subscription with appropriate permissions
- Docker images for the application components (or update the image variables)

## Deployment

### 1. Initialize Terraform

```bash
terraform init
```

### 2. Configure Variables

Create a `terraform.tfvars` file with your configuration:

```hcl
prefix                  = "ghdemo"
location                = "germanywestcentral"
azure_openai_api_key    = "your-openai-api-key"
azure_openai_endpoint   = "https://your-openai-instance.openai.azure.com/"
WORKER_IMAGE            = "your-registry/worker:tag"
FRONTEND_IMAGE          = "your-registry/frontend:tag"
API_STATUS_IMAGE        = "your-registry/api-status:tag"
API_PROCESSING_IMAGE    = "your-registry/api-processing:tag"
PERFTEST_IMAGE          = "your-registry/perftest:tag"
```

### 3. Plan Deployment

Review the planned changes:

```bash
terraform plan
```

### 4. Apply Configuration

Deploy the infrastructure:

```bash
terraform apply
```

### 5. Access the Application

After deployment, get the frontend URL:

```bash
terraform output
```

Or query the specific container app:

```bash
az containerapp show --name ca-frontend-<base-name> --resource-group rg-<base-name> --query properties.configuration.ingress.fqdn
```

## Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `prefix` | string | `ghdemo` | Prefix for resource names (2-4 lowercase chars) |
| `location` | string | `germanywestcentral` | Azure region for deployment |
| `azure_openai_api_key` | string | - | API key for Azure OpenAI (sensitive) |
| `azure_openai_endpoint` | string | - | Endpoint URL for Azure OpenAI |
| `WORKER_IMAGE` | string | - | Docker image tag for worker container |
| `FRONTEND_IMAGE` | string | - | Docker image tag for frontend container |
| `API_STATUS_IMAGE` | string | - | Docker image tag for API status container |
| `API_PROCESSING_IMAGE` | string | - | Docker image tag for API processing container |
| `PERFTEST_IMAGE` | string | - | Docker image tag for perftest job |

## Container App Environment Variables

### Frontend
| Variable | Source | Description |
|----------|--------|-------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Connection string for telemetry |
| `REACT_APP_PROCESS_API_URL` | API Processing FQDN | URL for processing API |

### API Processing
| Variable | Source | Description |
|----------|--------|-------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Connection string for telemetry |
| `CORS_ORIGIN` | Static | CORS allowed origins |
| `STORAGE_ACCOUNT_URL` | Storage Account | Blob storage endpoint |
| `STORAGE_CONTAINER` | Storage Container | Container name for blobs |
| `PROCESSED_BASE_URL` | API Status FQDN | Status API URL |
| `SERVICEBUS_FQDN` | Service Bus | Service Bus namespace FQDN |
| `SERVICEBUS_QUEUE` | Service Bus Queue | Queue name |
| `AZURE_CLIENT_ID` | Managed Identity | Client ID for authentication |

### API Status
| Variable | Source | Description |
|----------|--------|-------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Connection string for telemetry |
| `CORS_ORIGIN` | Static | CORS allowed origins |
| `COSMOS_ACCOUNT_URL` | Cosmos DB | Cosmos DB endpoint |
| `COSMOS_DB_NAME` | Cosmos Database | Database name |
| `COSMOS_CONTAINER_NAME` | Cosmos Container | Container name |
| `AZURE_CLIENT_ID` | Managed Identity | Client ID for authentication |

### Worker
| Variable | Source | Description |
|----------|--------|-------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Connection string for telemetry |
| `STORAGE_ACCOUNT_URL` | Storage Account | Blob storage endpoint |
| `STORAGE_CONTAINER` | Storage Container | Container name for blobs |
| `SERVICEBUS_FQDN` | Service Bus | Service Bus namespace FQDN |
| `SERVICEBUS_QUEUE` | Service Bus Queue | Queue name |
| `AZURE_CLIENT_ID` | Managed Identity | Client ID for authentication |
| `BATCH_SIZE` | Static | Message batch size (10) |
| `BATCH_MAX_WAIT_TIME` | Static | Max wait time in seconds (1) |
| `AZURE_OPENAI_API_KEY` | Variable | OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Variable | OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Static | Deployment name (gpt-4o-mini) |
| `COSMOS_ACCOUNT_URL` | Cosmos DB | Cosmos DB endpoint |
| `COSMOS_DB_NAME` | Cosmos Database | Database name |
| `COSMOS_CONTAINER_NAME` | Cosmos Container | Container name |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | Static | Enable GenAI content capture |

## State Management

The project is configured with Azure backend for remote state storage:

```hcl
backend "azurerm" {
  resource_group_name  = "rg-base"
  storage_account_name = "tomaskubicatf"
  container_name       = "tfstate"
  key                  = "gh-copilot-demo.tfstate"
  use_azuread_auth     = true
  subscription_id      = "673af34d-6b28-41dc-bc7b-f507418045e6"
}
```

To use local state instead, change the backend in `providers.tf` to `backend "local" {}`.

## Security Considerations

### For Learning Environment
- Public network access enabled for easier testing
- CORS set to `*` for development convenience
- Firewall rules open for PostgreSQL (if applicable)

### For Production Use
Consider implementing:
- Private endpoints for Azure services
- Network security groups and virtual network integration
- Restricted CORS policies
- Azure Key Vault for secrets management
- Azure Front Door or Application Gateway for WAF
- Private container registries
- Disable public access to storage accounts
- Enable soft delete and versioning on storage
- Implement backup and disaster recovery
- Add tags for cost management

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

⚠️ **Warning**: This will permanently delete all resources and data. Ensure you have backups if needed.

## Provider Versions

- `hashicorp/azurerm`: ~> 4.0
- `hashicorp/random`: ~> 3.0
- `hashicorp/archive`: ~> 2.0
- `Azure/azapi`: ~> 2.0
- `hashicorp/time`: ~> 0.0

## Notes

- Resources are named with a random suffix for uniqueness: `{prefix}-{random}`
- All container apps use user-assigned managed identity for secure authentication
- Container Apps automatically scale based on workload (worker scales on queue depth)
- The infrastructure uses OAuth/Entra ID authentication where possible (no connection strings)

## TODO

For enterprise production use, consider adding:

- [ ] CI/CD pipeline using GitHub Actions
- [ ] Infrastructure as Code security scanning (Checkov, tfsec, Trivy)
- [ ] FinOps tagging and cost management
- [ ] Multi-environment setup (dev, staging, prod)
- [ ] Network isolation with VNets and private endpoints
- [ ] Azure Key Vault integration for secrets
- [ ] Backup and disaster recovery configuration
- [ ] Monitoring alerts and dashboards
- [ ] Log retention policies
- [ ] Compliance and governance policies
