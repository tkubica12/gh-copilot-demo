resource "helm_release" "demo" {
  name      = "demo"
  chart     = "../charts/demo"
  namespace = "default"

  depends_on = [azurerm_kubernetes_cluster.main]
}

output "helm_release_name" {
  value       = helm_release.demo.name
  description = "Name of the deployed Helm release"
}

output "helm_release_namespace" {
  value       = helm_release.demo.namespace
  description = "Namespace where the Helm release is deployed"
}

output "helm_release_status" {
  value       = helm_release.demo.status
  description = "Status of the Helm release"
}
