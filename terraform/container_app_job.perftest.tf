resource "azurerm_container_app_job" "perftest" {
  name                         = "ca-job-perftest-${local.base_name}"
  location                     = azurerm_resource_group.main.location
  resource_group_name          = azurerm_resource_group.main.name
  container_app_environment_id = azurerm_container_app_environment.main.id

  replica_timeout_in_seconds = 3600
  replica_retry_limit        = 3

  manual_trigger_config {
    parallelism              = 1
    replica_completion_count = 1
  }

  template {
    container {
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-async-perftest:latest"
      name   = "perftest"
      cpu    = 1
      memory = "2Gi"

      env {
        name  = "TEST_URL"
        value = "https://${azapi_resource.api_processing.output.properties.configuration.ingress.fqdn}"
      }
    }
  }
}
