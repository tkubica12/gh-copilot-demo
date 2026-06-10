# Azure Monitor Workspace for managed Prometheus
resource "azurerm_monitor_workspace" "main" {
  name                = "amw-${local.base_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

# Azure Managed Grafana
resource "azurerm_dashboard_grafana" "main" {
  name                              = "grafana-${local.base_name}"
  resource_group_name               = azurerm_resource_group.main.name
  location                          = azurerm_resource_group.main.location
  api_key_enabled                   = true
  deterministic_outbound_ip_enabled = false
  public_network_access_enabled     = true

  identity {
    type = "SystemAssigned"
  }

  azure_monitor_workspace_integrations {
    resource_id = azurerm_monitor_workspace.main.id
  }
}

# Grant Grafana access to read from Monitor Workspace
resource "azurerm_role_assignment" "grafana_monitoring_reader" {
  scope                = azurerm_monitor_workspace.main.id
  role_definition_name = "Monitoring Data Reader"
  principal_id         = azurerm_dashboard_grafana.main.identity[0].principal_id
}

# Data Collection Endpoint for Prometheus scraping
resource "azurerm_monitor_data_collection_endpoint" "prometheus" {
  name                = "dce-prometheus-${local.base_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  kind                = "Linux"
}

# Data Collection Rule for Prometheus scraping
resource "azurerm_monitor_data_collection_rule" "prometheus" {
  name                        = "dcr-prometheus-${local.base_name}"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.prometheus.id

  destinations {
    monitor_account {
      monitor_account_id = azurerm_monitor_workspace.main.id
      name               = "MonitoringAccount"
    }
  }

  data_flow {
    streams      = ["Microsoft-PrometheusMetrics"]
    destinations = ["MonitoringAccount"]
  }

  data_sources {
    prometheus_forwarder {
      streams = ["Microsoft-PrometheusMetrics"]
      name    = "PrometheusDataSource"
    }
  }

  description = "Data collection rule for Prometheus metrics"
}

# Associate DCR with AKS cluster
resource "azurerm_monitor_data_collection_rule_association" "prometheus_aks" {
  name                    = "dcra-prometheus-aks-${local.base_name}"
  target_resource_id      = azurerm_kubernetes_cluster.main.id
  data_collection_rule_id = azurerm_monitor_data_collection_rule.prometheus.id
}
