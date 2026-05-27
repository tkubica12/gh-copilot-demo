output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "aks_cluster_name" {
  description = "Name of the AKS cluster"
  value       = azurerm_kubernetes_cluster.main.name
}

output "grafana_endpoint" {
  description = "Endpoint URL for Azure Managed Grafana"
  value       = azurerm_dashboard_grafana.main.endpoint
}

output "grafana_id" {
  description = "Resource ID of Azure Managed Grafana"
  value       = azurerm_dashboard_grafana.main.id
}

output "monitor_workspace_id" {
  description = "Resource ID of Azure Monitor Workspace"
  value       = azurerm_monitor_workspace.main.id
}

output "prometheus_query_endpoint" {
  description = "Query endpoint for Prometheus in Azure Monitor Workspace"
  value       = azurerm_monitor_workspace.main.query_endpoint
}
