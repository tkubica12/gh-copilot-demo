resource "azapi_resource" "api_frontend" {
  type      = "Microsoft.App/containerApps@2024-10-02-preview"
  name      = "ca-frontend-${local.base_name}"
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
        }
      }
      template = {
        containers = [
          {
            name  = "myapp"
            image = var.FRONTEND_IMAGE
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
                name  = "REACT_APP_PROCESS_API_URL"
                value = "https://${azapi_resource.api_processing.output.properties.configuration.ingress.fqdn}/api/process"

              }
            ]
          }
        ]
        scale = {
          minReplicas = 1
          maxReplicas = 5
        }
      }
    }
  }
  response_export_values = ["*"]
}
