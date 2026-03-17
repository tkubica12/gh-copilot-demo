# Azure Container Apps Demo Infrastructure

This folder contains a standalone Terraform configuration that deploys a demo workload on Azure. The stack is centered on Azure Container Apps and supporting platform services for storage, messaging, observability, identity, and persistence.

The deployment creates a small document-processing platform composed of:

- a frontend web application
- an API for document submission and processing orchestration
- an API for status lookup
- a background worker that consumes queue messages and uses Azure OpenAI
- a manual performance-test job
- shared Azure services for storage, Service Bus, Cosmos DB, logging, and managed identity

## What This Project Deploys

At a high level, the infrastructure flow is:

1. A user interacts with the frontend Container App.
2. The frontend calls the processing API.
3. The processing API stores data in Blob Storage and sends work items to Service Bus.
4. The worker scales based on queue depth, consumes messages, uses Azure OpenAI, and writes status data to Cosmos DB.
5. The status API reads document status from Cosmos DB.
6. Application telemetry is sent to Application Insights and Log Analytics.

## Architecture Summary

### Runtime components

| Component | Terraform resource | Exposure | Image variable | Purpose |
| --- | --- | --- | --- | --- |
| Frontend | `azapi_resource.api_frontend` | External HTTP on port 80 | `FRONTEND_IMAGE` | User-facing web UI |
| Processing API | `azapi_resource.api_processing` | External HTTP on port 80 | `API_PROCESSING_IMAGE` | Accepts work requests, writes to storage, enqueues messages |
| Status API | `azapi_resource.api_status` | External HTTP on port 80 | `API_STATUS_IMAGE` | Returns processing status from Cosmos DB |
| Worker | `azapi_resource.api_worker` | Internal only | `WORKER_IMAGE` | Consumes Service Bus queue messages and performs background processing |
| Performance test job | `azurerm_container_app_job.perftest` | Manual trigger | `PERFTEST_IMAGE` | Runs load or smoke tests against the processing API |

### Shared Azure services

| Service | Terraform resource | Purpose |
| --- | --- | --- |
| Resource Group | `azurerm_resource_group.main` | Deployment boundary for the demo stack |
| Managed Identity | `azurerm_user_assigned_identity.main` | Shared user-assigned identity used by the apps |
| Container Apps Environment | `azurerm_container_app_environment.main` | Shared hosting environment for the apps and job |
| Log Analytics Workspace | `azurerm_log_analytics_workspace.main` | Central log storage |
| Application Insights | `azurerm_application_insights.main` | Application telemetry |
| Storage Account | `azurerm_storage_account.main` | Blob storage for uploaded or generated artifacts |
| Storage Container | `azurerm_storage_container.main` | Blob container named `data` |
| Service Bus Namespace | `azurerm_servicebus_namespace.main` | Messaging namespace |
| Service Bus Queue | `azurerm_servicebus_queue.main` | Queue named `documents-to-process` |
| Cosmos DB Account | `azurerm_cosmosdb_account.main` | Serverless NoSQL account |
| Cosmos DB SQL Database | `azurerm_cosmosdb_sql_database.main` | Database named `mydb` |
| Cosmos DB SQL Container | `azurerm_cosmosdb_sql_container.main` | Container named `mydocuments` with partition key `/id` |

## File-by-File Layout

| File | Responsibility |
| --- | --- |
| `providers.tf` | Provider requirements, AzureRM backend configuration, provider features |
| `variables.tf` | Input variables for region, Azure OpenAI, and container images |
| `locals.tf` | Common naming locals based on the prefix and random suffix |
| `main.tf` | Resource group, random suffix, current Azure client context |
| `identity.tf` | Shared user-assigned managed identity |
| `monitoring.tf` | Log Analytics and Application Insights |
| `container_app_env.tf` | Azure Container Apps managed environment |
| `storage.tf` | Storage account and blob container |
| `service_bus.tf` | Service Bus namespace and queue |
| `cosmos.tf` | Cosmos DB account, database, and container |
| `rbac.tf` | Role assignments and Cosmos DB data-plane authorization |
| `container_app.frontend.tf` | Frontend Container App |
| `container_app.api-processing.tf` | Processing API Container App |
| `container_app.api-status.tf` | Status API Container App |
| `container_app.worker.tf` | Worker Container App with queue-based autoscaling |
| `container_app_job.perftest.tf` | Manual Container App Job for performance tests |
| `demo.auto.tfvars` | Example variable file for Azure OpenAI settings |

## Naming Convention

Resource names are derived from two locals:

- `local.base_name = "${replace(var.prefix, "_", "-")}-${random_string.main.result}"`
- `local.base_name_nodash = replace(local.base_name, "-", "")`

With the default prefix `ghdemo`, a deployment creates names similar to:

- Resource group: `rg-ghdemo-abcd`
- Container Apps environment: `cae-ghdemo-abcd`
- Managed identity: `ghdemo-abcd-identity`
- Storage account: `stghdemoabcd`
- Service Bus namespace: `sb-ghdemo-abcd`
- Cosmos DB account: `cosmos-ghdemo-abcd`

The random suffix avoids naming collisions across repeated demo deployments.

## Detailed Cloud Resource Inventory

### Core platform resources

| Resource type | Terraform name | Azure name pattern | Key settings |
| --- | --- | --- | --- |
| `azurerm_resource_group` | `main` | `rg-${local.base_name}` | Region from `var.location` |
| `azurerm_user_assigned_identity` | `main` | `${local.base_name}-identity` | Shared identity for apps |
| `azurerm_container_app_environment` | `main` | `cae-${local.base_name}` | Connected to Log Analytics |
| `azurerm_log_analytics_workspace` | `main` | `logs-${local.base_name}` | SKU `PerGB2018`, retention 30 days |
| `azurerm_application_insights` | `main` | `ai-${local.base_name}` | `application_type = "web"` |

### Data and messaging resources

| Resource type | Terraform name | Azure name pattern | Key settings |
| --- | --- | --- | --- |
| `azurerm_storage_account` | `main` | `st${local.base_name_nodash}` | Standard LRS, OAuth default, local users disabled |
| `azurerm_storage_container` | `main` | `data` | Blob container for artifacts |
| `azurerm_servicebus_namespace` | `main` | `sb-${local.base_name}` | Standard SKU, local auth disabled |
| `azurerm_servicebus_queue` | `main` | `documents-to-process` | Partitioning enabled |
| `azurerm_cosmosdb_account` | `main` | `cosmos-${local.base_name}` | Serverless, session consistency, local auth disabled |
| `azurerm_cosmosdb_sql_database` | `main` | `mydb` | SQL API database |
| `azurerm_cosmosdb_sql_container` | `main` | `mydocuments` | Partition key `/id` |

### Application runtime resources

| Resource type | Terraform name | Azure name pattern | Key settings |
| --- | --- | --- | --- |
| `azapi_resource` | `api_frontend` | `ca-frontend-${local.base_name}` | External ingress, 0.25 CPU, 0.5 GiB RAM, 1-5 replicas |
| `azapi_resource` | `api_processing` | `ca-api-processing-${local.base_name}` | External ingress, CORS `*`, 0.25 CPU, 0.5 GiB RAM, 1-5 replicas |
| `azapi_resource` | `api_status` | `ca-api-status-${local.base_name}` | External ingress, CORS `*`, 0.25 CPU, 0.5 GiB RAM, 1-5 replicas |
| `azapi_resource` | `api_worker` | `ca-worker-${local.base_name}` | No ingress, queue autoscaling, 0.25 CPU, 0.5 GiB RAM, 1-5 replicas |
| `azurerm_container_app_job` | `perftest` | `ca-job-perftest-${local.base_name}` | Manual trigger, timeout 3600 seconds, retry limit 3 |

### Authorization resources

| Resource type | Terraform name | Role or purpose |
| --- | --- | --- |
| `azurerm_role_assignment` | `self_storage` | Current user gets `Storage Blob Data Owner` on the storage account |
| `azurerm_role_assignment` | `app_storage` | Managed identity gets `Storage Blob Data Contributor` on the storage account |
| `azurerm_role_assignment` | `self_controlplane_storage` | Current user gets `Storage Queue Data Contributor` on the storage account |
| `azurerm_role_assignment` | `self_servicebus_sender` | Current user gets `Azure Service Bus Data Sender` |
| `azurerm_role_assignment` | `app_servicebus_sender` | Managed identity gets `Azure Service Bus Data Sender` |
| `azurerm_role_assignment` | `self_servicebus_receiver` | Current user gets `Azure Service Bus Data Receiver` |
| `azurerm_role_assignment` | `app_servicebus_receiver` | Managed identity gets `Azure Service Bus Data Receiver` |
| `azurerm_cosmosdb_sql_role_definition` | `main` | Custom Cosmos DB role named `mywriter` |
| `azurerm_cosmosdb_sql_role_assignment` | `self` | Current user gets the custom Cosmos DB role |
| `azurerm_cosmosdb_sql_role_assignment` | `app` | Managed identity gets the custom Cosmos DB role |

## Application Configuration and Dependencies

### Frontend Container App

Purpose:
Expose the user-facing web application and direct requests to the processing API.

Key configuration:

- external ingress enabled on port 80
- single active revision mode
- 1 to 5 replicas
- Application Insights connection string injected as an environment variable
- `REACT_APP_PROCESS_API_URL` points to the processing API FQDN plus `/api/process`

Dependencies:

- Container Apps environment
- Application Insights
- Processing API FQDN
- Managed identity assignment

### Processing API Container App

Purpose:
Receive processing requests, store payloads in Blob Storage, and publish messages to Service Bus.

Key configuration:

- external ingress enabled on port 80
- CORS currently configured as `*`
- 1 to 5 replicas
- polling interval 5 seconds
- cooldown period 60 seconds

Environment variables injected by Terraform:

- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `CORS_ORIGIN`
- `STORAGE_ACCOUNT_URL`
- `STORAGE_CONTAINER`
- `PROCESSED_BASE_URL`
- `SERVICEBUS_FQDN`
- `SERVICEBUS_QUEUE`
- `AZURE_CLIENT_ID`

Dependencies:

- Blob Storage
- Service Bus queue
- Status API FQDN
- Managed identity RBAC for Service Bus and Storage

### Status API Container App

Purpose:
Read document status information from Cosmos DB.

Key configuration:

- external ingress enabled on port 80
- CORS currently configured as `*`
- 1 to 5 replicas
- polling interval 5 seconds
- cooldown period 60 seconds

Environment variables injected by Terraform:

- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `CORS_ORIGIN`
- `AZURE_CLIENT_ID`
- `COSMOS_ACCOUNT_URL`
- `COSMOS_DB_NAME`
- `COSMOS_CONTAINER_NAME`
- `RETRY_AFTER`

Dependencies:

- Cosmos DB account, database, and container
- Managed identity Cosmos DB data-plane role

### Worker Container App

Purpose:
Consume queued work items, interact with Blob Storage and Cosmos DB, and call Azure OpenAI.

Key configuration:

- no public ingress
- single active revision mode
- user-assigned identity lifecycle configured for all operations
- 1 to 5 replicas
- queue-based custom autoscaling rule named `queue-scaling`
- worker scales when Service Bus message count reaches `5`

Environment variables injected by Terraform:

- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `STORAGE_ACCOUNT_URL`
- `STORAGE_CONTAINER`
- `SERVICEBUS_FQDN`
- `SERVICEBUS_QUEUE`
- `AZURE_CLIENT_ID`
- `BATCH_SIZE`
- `BATCH_MAX_WAIT_TIME`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `COSMOS_ACCOUNT_URL`
- `COSMOS_DB_NAME`
- `COSMOS_CONTAINER_NAME`
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`

Dependencies:

- Blob Storage
- Service Bus queue and namespace
- Cosmos DB account, database, and container
- Azure OpenAI endpoint and API key
- Managed identity RBAC for Storage, Service Bus, and Cosmos DB

### Performance Test Job

Purpose:
Run manual traffic generation or validation against the processing API.

Key configuration:

- Container App Job instead of a long-running app
- manual trigger
- parallelism 1
- completion count 1
- timeout 3600 seconds
- retry limit 3
- `TEST_URL` points at the processing API base URL

Dependencies:

- Container Apps environment
- Processing API FQDN

## Variables

The module exposes the following input variables.

| Variable | Type | Required | Sensitive | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `prefix` | `string` | No | No | `ghdemo` | Prefix used in generated Azure resource names. Intended to be short, lowercase, and simple. |
| `location` | `string` | No | No | `germanywestcentral` | Azure region for all resources. |
| `azure_openai_api_key` | `string` | Yes | Yes | None | API key used by the worker to access Azure OpenAI. |
| `azure_openai_endpoint` | `string` | Yes | No | None | Endpoint URL for Azure OpenAI. |
| `WORKER_IMAGE` | `string` | Yes | No | None | Full image reference for the worker container. |
| `FRONTEND_IMAGE` | `string` | Yes | No | None | Full image reference for the frontend container. |
| `API_STATUS_IMAGE` | `string` | Yes | No | None | Full image reference for the status API container. |
| `API_PROCESSING_IMAGE` | `string` | Yes | No | None | Full image reference for the processing API container. |
| `PERFTEST_IMAGE` | `string` | Yes | No | None | Full image reference for the perftest job container. |

### Example variable file

Use a local `terraform.auto.tfvars` or environment-specific `.tfvars` file. Do not commit secrets.

```hcl
prefix                = "ghdemo"
location              = "germanywestcentral"
azure_openai_api_key  = "replace-me"
azure_openai_endpoint = "https://your-openai-resource.openai.azure.com"

WORKER_IMAGE         = "myregistry.azurecr.io/demo/worker:latest"
FRONTEND_IMAGE       = "myregistry.azurecr.io/demo/frontend:latest"
API_STATUS_IMAGE     = "myregistry.azurecr.io/demo/api-status:latest"
API_PROCESSING_IMAGE = "myregistry.azurecr.io/demo/api-processing:latest"
PERFTEST_IMAGE       = "myregistry.azurecr.io/demo/perftest:latest"
```

### About `demo.auto.tfvars`

This folder currently includes `demo.auto.tfvars` with Azure OpenAI values. Treat that file as demo-only input. For real deployments:

1. replace the values with your own tenant-specific settings
2. avoid storing secrets in version control
3. prefer a local untracked tfvars file, CI secret variables, or a secret store such as Azure Key Vault

## Identity and Access Model

The deployment uses a single user-assigned managed identity across the applications.

The managed identity receives:

- `Storage Blob Data Contributor` on the storage account
- `Azure Service Bus Data Sender` on the Service Bus namespace
- `Azure Service Bus Data Receiver` on the Service Bus namespace
- a custom Cosmos DB SQL role that permits container operations and metadata read access

The current Terraform operator also receives access so the deployed services can be exercised manually after provisioning.

### Important authentication behavior

- Blob Storage is configured with OAuth as the default authentication method.
- Service Bus has local authentication disabled.
- Cosmos DB has local authentication disabled.
- The applications are expected to use Entra ID and the managed identity rather than connection strings.

## Provider and Backend Configuration

### Required providers

The Terraform configuration requires:

- `hashicorp/azurerm` `~> 4`
- `hashicorp/random` `~> 3`
- `hashicorp/archive` `~> 2`
- `Azure/azapi` `~> 2`
- `hashicorp/time` `~> 0`

Note that `archive` and `time` are declared but are not currently used by the resources in this folder.

### Default backend

The configuration uses an AzureRM remote backend in `providers.tf` with hardcoded values:

- resource group: `rg-base`
- storage account: `tomaskubicatf`
- container: `tfstate`
- state key: `gh-copilot-demo.tfstate`
- subscription ID: `673af34d-6b28-41dc-bc7b-f507418045e6`

This works only if you have access to that backend storage account and subscription.

### Deployment options

You have two practical ways to deploy:

1. Use the existing backend configuration if you have access to the referenced Azure resources.
2. Reconfigure the backend for your own Azure Storage account, or temporarily switch to a local backend for isolated testing.

## Prerequisites

Before deployment, make sure the following are in place:

1. Terraform installed locally.
2. Azure CLI installed and authenticated.
3. Access to an Azure subscription where you can create resource groups, RBAC assignments, Container Apps resources, Cosmos DB, Service Bus, Storage, and monitoring resources.
4. Four application container images and one test-job image built and published to a registry reachable by Azure Container Apps.
5. An Azure OpenAI resource with a valid endpoint and API key.
6. If using the default backend, access to the state storage account and container defined in `providers.tf`.
7. If using a private registry, appropriate image pull permissions for Container Apps.

## How to Deploy

### 1. Authenticate to Azure

```powershell
az login
az account set --subscription <your-subscription-id>
```

If you keep the default `providers.tf` subscription ID, make sure it matches the Azure account you intend to use.

### 2. Prepare variables

Create a local tfvars file or export variables through your CI system.

Example local file:

```powershell
Copy-Item .\demo.auto.tfvars .\terraform.auto.tfvars
```

Then edit `terraform.auto.tfvars` to set:

- your Azure OpenAI endpoint
- your Azure OpenAI API key
- all five container image references
- an optional custom `prefix` and `location`

### 3. Initialize Terraform

#### Option A: use the existing remote backend

```powershell
terraform -chdir=examples/terraform init
```

#### Option B: point the backend to your own Azure Storage account

```powershell
terraform -chdir=examples/terraform init -reconfigure `
  -backend-config="resource_group_name=<rg-name>" `
  -backend-config="storage_account_name=<storage-account-name>" `
  -backend-config="container_name=tfstate" `
  -backend-config="key=gh-copilot-demo.tfstate" `
  -backend-config="subscription_id=<subscription-id>" `
  -backend-config="use_azuread_auth=true"
```

#### Option C: switch to local state for an isolated demo

The comment in `providers.tf` indicates that the backend can be changed to `local`. If you choose this route, modify the backend block accordingly before running init.

```powershell
terraform -chdir=examples/terraform init -reconfigure
```

### 4. Validate the configuration

```powershell
terraform -chdir=examples/terraform fmt -check
terraform -chdir=examples/terraform validate
```

### 5. Review the execution plan

```powershell
terraform -chdir=examples/terraform plan
```

Review the following carefully:

- target subscription and region
- generated resource names
- container image references
- Azure OpenAI endpoint
- RBAC assignments being created

### 6. Apply the deployment

```powershell
terraform -chdir=examples/terraform apply
```

### 7. Discover deployed endpoints

This module does not currently define Terraform outputs. After deployment, obtain the generated FQDNs from Azure Container Apps.

Example:

```powershell
az containerapp list -g <resource-group-name> -o table
```

Useful app names follow these patterns:

- `ca-frontend-<suffix>`
- `ca-api-processing-<suffix>`
- `ca-api-status-<suffix>`
- `ca-worker-<suffix>`
- `ca-job-perftest-<suffix>`

## Post-Deployment Validation

Use the following checks after a successful apply.

### Infrastructure checks

1. Confirm all resources were created in the expected resource group.
2. Confirm the Container Apps environment exists and the apps are healthy.
3. Confirm the Service Bus queue exists.
4. Confirm the Blob container `data` exists.
5. Confirm the Cosmos DB database `mydb` and container `mydocuments` exist.

### Application checks

1. Open the frontend URL and verify the UI loads.
2. Call the processing API and verify it accepts requests.
3. Confirm the processing API enqueues messages into Service Bus.
4. Confirm the worker processes queued messages.
5. Call the status API and verify status entries are returned from Cosmos DB.
6. Verify telemetry appears in Application Insights or Log Analytics.

### Performance-test job

The performance-test job is created but not run automatically. Trigger it manually when needed.

Example CLI workflow:

```powershell
az containerapp job start --name <job-name> --resource-group <resource-group-name>
```

## Operational Notes

### Scaling

- frontend, processing API, and status API scale between 1 and 5 replicas
- worker scales between 1 and 5 replicas and has a custom Service Bus scaling rule
- the worker rule uses a queue message threshold of `5`
- the perftest job is manual and does not run on a schedule

### Observability

- the Container Apps environment sends platform logs to Log Analytics
- every runtime component receives the Application Insights connection string
- the worker enables `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`

### Security and limitations

This configuration is appropriate for demo and learning scenarios, but it has gaps you should address before any production use:

1. `demo.auto.tfvars` should not contain real secrets in source control.
2. Azure OpenAI credentials are passed as plain environment variables to the worker.
3. The APIs allow CORS from `*`.
4. No private networking, private endpoints, or ingress restrictions are defined.
5. No health probes are defined for the Container Apps.
6. No Terraform outputs are defined for app URLs or resource identifiers.
7. Backend configuration is tied to a specific subscription and storage account unless reconfigured.

Recommended next hardening steps:

1. move secrets to Azure Key Vault or a secure deployment pipeline
2. narrow CORS origins to known frontend hosts
3. add Terraform outputs for app FQDNs and key resource names
4. add health probes to the container apps
5. consider private endpoints and network isolation for stateful services
6. split backend configuration from source-controlled defaults

## How to Destroy

When the environment is no longer needed:

```powershell
terraform -chdir=examples/terraform destroy
```

Make sure you are targeting the correct subscription, backend, and state file before running destroy.

## Quick Reference

### Required inputs

- `azure_openai_api_key`
- `azure_openai_endpoint`
- `WORKER_IMAGE`
- `FRONTEND_IMAGE`
- `API_STATUS_IMAGE`
- `API_PROCESSING_IMAGE`
- `PERFTEST_IMAGE`

### Optional inputs

- `prefix`
- `location`

### Main Azure services used

- Azure Resource Group
- Azure Container Apps Environment
- Azure Container Apps
- Azure Container Apps Job
- Azure Monitor Log Analytics
- Azure Application Insights
- Azure Storage Account and Blob Container
- Azure Service Bus Namespace and Queue
- Azure Cosmos DB for NoSQL
- Azure User-Assigned Managed Identity
- Azure OpenAI