resource "azapi_resource" "api_processing" {
  type      = "Microsoft.App/containerApps@2024-10-02-preview"
  name      = "ca-api-processing-${local.base_name}"
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
            image = var.API_PROCESSING_IMAGE
            resources = {
              cpu    = 0.5
              memory = "1Gi"
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
                name  = "STORAGE_ACCOUNT_URL"
                value = azurerm_storage_account.main.primary_blob_endpoint
              },
              {
                name  = "STORAGE_CONTAINER"
                value = azurerm_storage_container.main.name
              },
              {
                name  = "PROCESSED_BASE_URL"
                value = "https://${azapi_resource.api_status.output.properties.configuration.ingress.fqdn}/api/status"
              },
              {
                name  = "SERVICEBUS_FQDN"
                value = replace(replace(azurerm_servicebus_namespace.main.endpoint, "https://", ""), ":443/", "")
              },
              {
                name  = "SERVICEBUS_QUEUE"
                value = azurerm_servicebus_queue.main.name
              },
              {
                name  = "AZURE_CLIENT_ID"
                value = azurerm_user_assigned_identity.main.client_id
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
