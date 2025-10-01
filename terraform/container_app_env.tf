resource "azurerm_container_app_environment" "main" {
  name                       = "cae-${local.base_name}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

resource "azapi_update_resource" "container_app_env_prometheus" {
  type        = "Microsoft.App/managedEnvironments@2024-03-01"
  resource_id = azurerm_container_app_environment.main.id

  body = {
    properties = {
      appLogsConfiguration = {
        destination = "azure-monitor"
      }
      openTelemetryConfiguration = {
        destinationsConfiguration = {
          otlpConfigurations = [
            {
              name     = "prometheus"
              endpoint = "${azurerm_monitor_workspace.main.query_endpoint}v1/otlp"
            }
          ]
        }
        tracesConfiguration = {
          destinations = ["prometheus"]
        }
        metricsConfiguration = {
          destinations = ["prometheus"]
        }
      }
    }
  }

  depends_on = [
    azurerm_container_app_environment.main,
    azurerm_monitor_workspace.main
  ]
}
