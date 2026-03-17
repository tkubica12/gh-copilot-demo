# MCP demo

## How to start random_string_mcp

This repository contains a small local MCP server in `mcp\random_string_mcp` that is wired into `.vscode\mcp.json` as `my-mcp-string-generator`.

It is implemented with `FastMCP` and exposes two tools:

- `random_string`: generate a random string from selected character classes
- `unique_string`: generate a deterministic string from a seed value

1. Open a terminal and navigate to the `random_string_mcp\src` directory:
   ```pwsh
   cd .\random_string_mcp\src
   ```
2. Start the MCP server using `uv`:
   ```pwsh
   uv run main.py
   ```

The server runs over SSE and is exposed at `http://127.0.0.1:8000/sse`.

Once it is running, Copilot can use it through the workspace MCP configuration.

Example prompt:

```text
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers.
```

## How to deploy infrastructure (AKS, etc.)

1. Navigate to the `mcp/demo_infra` directory:
   ```pwsh
   cd demo_infra
   ```
2. Initialize Terraform:
   ```pwsh
   terraform init
   ```
3. Review the plan:
   ```pwsh
   terraform plan
   ```
4. Apply the infrastructure changes:
   ```pwsh
   terraform apply -auto-approve
   ```

## How to get AKS credentials using Azure CLI

1. Make sure you are logged in to Azure:
   ```pwsh
   az login
   ```
2. Set your subscription (if needed):
   ```pwsh
   az account set --subscription <your-subscription-id>
   ```
3. Get AKS credentials (replace `<resource-group>` and `<aks-name>`):
   ```pwsh
   az aks get-credentials --resource-group <resource-group> --name <aks-name>
   ```

## How to deploy the Helm chart

1. Navigate to the Helm chart directory:
   ```pwsh
   cd ../charts/demo
   ```
2. Deploy the chart (replace `<release-name>` and `<namespace>` as needed):
   ```pwsh
   helm install <release-name> .
   # Or to upgrade if already installed:
   helm upgrade <release-name> .
   ```
3. (Optional) To use a custom values file:
   ```pwsh
   helm install <release-name> . -f values.yaml
   ```

This will create the namespaces, deployments, services, service accounts, configmaps, and secrets as described in the chart.
