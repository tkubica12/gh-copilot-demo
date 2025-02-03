resource "azapi_resource" "api_status" {
  type      = "Microsoft.App/containerApps@2024-10-02-preview"
  name      = "ca-api-status-${local.base_name}"
  parent_id = azurerm_resource_group.main.id
  location  = azurerm_resource_group.main.location

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }

  body = {
    properties = {
      managedEnvironmentId = azurerm_container_app_environment.main.id
      configuration = {
        activeRevisionsMode = "Single"
        ingress = {
          external   = true
          targetPort = 80
          traffic = [
            {
              latestRevision = true
              weight         = 100
            }
          ]
          corsPolicy = {
            allowedOrigins = ["*"]
          }
        }
      }
      template = {
        containers = [
          {
            name  = "myapp"
            image = "ghcr.io/tkubica12/azure-workshops/d-ai-async-api-status:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
            env = [
              {
                name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
                value = azurerm_application_insights.main.connection_string
              },
              {
                name  = "CORS_ORIGIN"
                value = "*"
              },
              {
                name  = "AZURE_CLIENT_ID"
                value = azurerm_user_assigned_identity.main.client_id
              },
              {
                name  = "COSMOS_ACCOUNT_URL"
                value = azurerm_cosmosdb_account.main.endpoint
              },
              {
                name  = "COSMOS_DB_NAME"
                value = azurerm_cosmosdb_sql_database.main.name
              },
              {
                name  = "COSMOS_CONTAINER_NAME"
                value = azurerm_cosmosdb_sql_container.main.name
              },
              {
                name  = "RETRY_AFTER"
                value = "1"
              }
            ]
          }
        ]
        scale = {
          minReplicas     = 1
          maxReplicas     = 5
          pollingInterval = 5
          cooldownPeriod  = 60
        }
      }
    }
  }
  response_export_values = ["*"]
}
