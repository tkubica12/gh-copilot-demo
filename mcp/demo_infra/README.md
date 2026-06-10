# Terraform Infrastructure - MCP Demo Environment

This Terraform project deploys infrastructure for the Model Context Protocol (MCP) demo, including an Azure Kubernetes Service (AKS) cluster, PostgreSQL database, and demo applications deployed via Helm charts.

## Project Overview

This infrastructure is designed to demonstrate MCP tools and capabilities with GitHub Copilot. It provides a Kubernetes environment with a managed PostgreSQL database and sample applications for testing MCP integrations.

## Architecture

The infrastructure deploys the following components:

```
┌─────────────────────────────────────┐
│      Azure Resource Group           │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   AKS Cluster                │  │
│  │   - 1 node (B2s)             │  │
│  │   - Azure Policy enabled     │  │
│  │   - Managed Identity         │  │
│  │                              │  │
│  │   ┌──────────────────────┐   │  │
│  │   │  Helm Release        │   │  │
│  │   │  (demo apps)         │   │  │
│  │   └──────────────────────┘   │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  PostgreSQL Flexible Server  │  │
│  │  - Burstable tier (B1ms)     │  │
│  │  - Public access enabled     │  │
│  │  - Version 16                │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  User Assigned Identity      │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Azure Resources

### Compute
- **Azure Kubernetes Service (AKS)** (`aks.tf`): Managed Kubernetes cluster
  - Single node pool with 1 node (`Standard_B2s` VM size)
  - Azure Policy integration enabled
  - User-assigned managed identity for cluster and kubelet
  - DNS prefix: `aks-{base_name}`

### Database
- **PostgreSQL Flexible Server** (`postgres.tf`): Managed PostgreSQL database
  - SKU: `B_Standard_B1ms` (Burstable tier for cost efficiency)
  - Storage: 32 GB
  - PostgreSQL version: 16
  - Backup retention: 7 days
  - Public network access enabled with firewall rule (0.0.0.0/0)
  - Random 24-character admin password generated

### Application Deployment
- **Helm Release** (`helm.tf`): Deploys demo applications to AKS
  - Chart location: `../charts/demo`
  - Namespace: `default`
  - Automatically deployed after AKS provisioning

### Security & Identity
- **User Assigned Managed Identity** (`identity.tf`): Managed identity for AKS cluster
  - Assigned to both AKS control plane and kubelet
  - Contributor role on resource group
- **RBAC Assignment** (`rbac.tf`): Resource group Contributor role for managed identity

### Supporting Resources
- **Resource Group** (`main.tf`): Container for all resources
- **Random String** (`main.tf`): 4-character random suffix for unique naming

## Project Structure

```
.
├── main.tf       # Resource group and base resources
├── providers.tf  # Terraform and provider configuration
├── variables.tf  # Input variables
├── locals.tf     # Local values for naming
├── identity.tf   # Managed identity
├── rbac.tf       # Role assignments
├── aks.tf        # Azure Kubernetes Service
├── postgres.tf   # PostgreSQL Flexible Server
└── helm.tf       # Helm release deployment
```

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed and authenticated
- [kubectl](https://kubernetes.io/docs/tasks/tools/) for Kubernetes cluster access
- [Helm](https://helm.sh/docs/intro/install/) for managing Kubernetes applications
- Azure subscription with appropriate permissions

## Deployment

### 1. Initialize Terraform

```bash
cd mcp/demo_infra
terraform init
```

### 2. Configure Variables (Optional)

Create a `terraform.tfvars` file to override defaults:

```hcl
prefix   = "mcp"
location = "swedencentral"
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

### 5. Get AKS Credentials

After deployment, configure kubectl to access the cluster:

```bash
az aks get-credentials \
  --resource-group rg-mcp-<random> \
  --name aks-mcp-<random> \
  --overwrite-existing
```

Replace `<random>` with the actual random suffix from your deployment.

### 6. Verify Deployment

Check cluster status:

```bash
kubectl cluster-info
kubectl get nodes
kubectl get pods -n default
```

### 7. Get Database Connection Details

Retrieve PostgreSQL connection information:

```bash
# Server FQDN
terraform output postgres_fqdn

# Admin username
terraform output postgres_admin_login

# Admin password (sensitive)
terraform output -raw postgres_admin_password
```

## Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `prefix` | string | `mcp` | Prefix for resource names (2-4 lowercase chars) |
| `location` | string | `swedencentral` | Azure region for deployment |

## Outputs

The following outputs are available after deployment:

### PostgreSQL Outputs
| Output | Description |
|--------|-------------|
| `postgres_server_name` | PostgreSQL Flexible Server name |
| `postgres_fqdn` | PostgreSQL Flexible Server FQDN |
| `postgres_admin_login` | PostgreSQL administrator username |
| `postgres_admin_password` | PostgreSQL administrator password (sensitive) |

### Helm Outputs
| Output | Description |
|--------|-------------|
| `helm_release_name` | Name of the deployed Helm release |
| `helm_release_namespace` | Namespace where Helm release is deployed |
| `helm_release_status` | Status of the Helm release |

## Connecting to PostgreSQL

Using psql:

```bash
# Get connection details
POSTGRES_HOST=$(terraform output -raw postgres_fqdn)
POSTGRES_USER=$(terraform output -raw postgres_admin_login)
POSTGRES_PASS=$(terraform output -raw postgres_admin_password)

# Connect
psql "host=$POSTGRES_HOST port=5432 dbname=postgres user=$POSTGRES_USER password=$POSTGRES_PASS sslmode=require"
```

Or export as environment variables for MCP tools:

```bash
export POSTGRES_HOST=$(terraform output -raw postgres_fqdn)
export POSTGRES_USER=$(terraform output -raw postgres_admin_login)
export POSTGRES_PASSWORD=$(terraform output -raw postgres_admin_password)
```

## Using with MCP Tools

This infrastructure is designed to work with MCP tools:

1. **Kubernetes MCP**: Connect to the AKS cluster to manage pods, deployments, and services
2. **Database MCP**: Connect to PostgreSQL for database operations and queries
3. **Azure MCP**: Query and manage Azure resources in the deployed resource group

### Example MCP Usage with GitHub Copilot

```
# Kubernetes operations
What namespaces do I have in my cluster?
Show me pods in default namespace
Get logs from the demo application

# Database operations
Connect to my PostgreSQL database and list all tables
Create a sample users table with some test data

# Azure resource queries
What is the status of my AKS cluster?
Show me the configuration of my PostgreSQL server
```

## State Management

This project uses local state management by default. The state file (`terraform.tfstate`) is stored in the project directory.

⚠️ **Note**: For team collaboration or production use, consider using remote state with Azure Storage:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "yourstorageaccount"
    container_name       = "tfstate"
    key                  = "mcp-demo.tfstate"
  }
}
```

## Security Considerations

### For Learning Environment
- Public network access enabled for PostgreSQL for easier testing
- Firewall rule allows all IPs (0.0.0.0/0) for database access
- Single node AKS cluster (no high availability)
- Burstable tier PostgreSQL (cost-optimized)

### For Production Use
Consider implementing:
- **Networking**: 
  - Virtual network integration for AKS and PostgreSQL
  - Private endpoints for database
  - Network security groups
  - Azure Firewall or Application Gateway
  
- **Security**:
  - Azure Key Vault for secrets management
  - Azure Active Directory integration for PostgreSQL
  - Restrict database firewall rules to specific IPs
  - Enable Azure Defender for Cloud
  - Pod security policies in Kubernetes
  
- **High Availability**:
  - Multi-node AKS cluster with multiple availability zones
  - PostgreSQL with geo-redundant backup
  - Multiple replicas for critical workloads
  
- **Monitoring**:
  - Azure Monitor for containers
  - Log Analytics workspace
  - Application Insights
  - Database monitoring and alerts
  
- **Compliance**:
  - Enable encryption at rest
  - Audit logging
  - Compliance tags and policies
  - Backup and disaster recovery plan

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

⚠️ **Warning**: This will permanently delete:
- The AKS cluster and all deployed applications
- The PostgreSQL database and all data
- All associated resources

Ensure you have backups of any important data before destroying.

## Provider Versions

- `hashicorp/azurerm`: ~> 4.0
- `hashicorp/random`: ~> 3.0
- `hashicorp/helm`: ~> 2.0

## Troubleshooting

### AKS Access Issues
If you cannot connect to the cluster:
```bash
# Verify cluster is running
az aks show --name aks-mcp-<random> --resource-group rg-mcp-<random>

# Re-fetch credentials
az aks get-credentials --name aks-mcp-<random> --resource-group rg-mcp-<random> --overwrite-existing
```

### PostgreSQL Connection Issues
If you cannot connect to PostgreSQL:
```bash
# Verify server is running
az postgres flexible-server show --name psql-mcp-<random> --resource-group rg-mcp-<random>

# Check firewall rules
az postgres flexible-server firewall-rule list --name psql-mcp-<random> --resource-group rg-mcp-<random>
```

### Helm Deployment Issues
If Helm deployment fails:
```bash
# Check Helm release status
helm list -n default

# Get release details
helm status demo -n default

# View release history
helm history demo -n default
```

## Notes

- Resources are named with format: `{prefix}-{random-suffix}`
- The 4-character random suffix ensures unique resource names
- AKS uses user-assigned managed identity for enhanced security
- PostgreSQL password is randomly generated and stored in Terraform state
- Helm chart must exist at `../charts/demo` relative to this directory

## TODO

For enterprise production use, consider adding:

- [ ] CI/CD pipeline using GitHub Actions
- [ ] Infrastructure as Code security scanning (Checkov, tfsec)
- [ ] Multi-environment configuration (dev, staging, prod)
- [ ] Virtual network integration
- [ ] Private endpoints for PostgreSQL
- [ ] Azure Key Vault for secrets
- [ ] Monitoring and alerting setup
- [ ] Backup and disaster recovery
- [ ] Cost management and tagging strategy
- [ ] GitOps with Flux or ArgoCD
- [ ] Ingress controller setup
- [ ] TLS certificate management
