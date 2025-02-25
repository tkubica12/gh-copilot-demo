resource "azapi_resource" "api_worker" {
  type      = "Microsoft.App/containerApps@2024-10-02-preview"
  name      = "ca-worker-${local.base_name}"
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
        identitySettings = [
          {
            identity  = azurerm_user_assigned_identity.main.id
            lifecycle = "All"
          }
        ]
      }
      template = {
        containers = [
          {
            name  = "myapp"
            image = var.WORKER_IMAGE
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
                name  = "STORAGE_ACCOUNT_URL"
                value = azurerm_storage_account.main.primary_blob_endpoint
              },
              {
                name  = "STORAGE_CONTAINER"
                value = azurerm_storage_container.main.name
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
              },
              {
                name  = "BATCH_SIZE"
                value = "10"
              },
              {
                name  = "BATCH_MAX_WAIT_TIME"
                value = "1"
              },
              {
                name  = "AZURE_OPENAI_API_KEY"
                value = var.azure_openai_api_key
              },
              {
                name  = "AZURE_OPENAI_ENDPOINT"
                value = var.azure_openai_endpoint
              },
              {
                name  = "AZURE_OPENAI_DEPLOYMENT_NAME"
                value = "gpt-4o-mini"
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
                name  = "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"
                value = "true"
              }
            ]
          }
        ]
        scale = {
          minReplicas     = 1
          maxReplicas     = 5
          pollingInterval = 5
          cooldownPeriod  = 60
          rules = [
            {
              name = "queue-scaling"
              custom = {
                type = "azure-servicebus"
                metadata = {
                  queueName    = azurerm_servicebus_queue.main.name
                  namespace    = azurerm_servicebus_namespace.main.name
                  messageCount = "5"
                }
                identity = azurerm_user_assigned_identity.main.id
              }
            }
          ]
        }
      }
    }
  }
  response_export_values = ["*"]
}
