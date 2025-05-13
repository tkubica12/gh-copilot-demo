resource "azurerm_kubernetes_cluster" "main" {
  name                 = "aks-${local.base_name}"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  dns_prefix           = "aks-${local.base_name}"
  azure_policy_enabled = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "UserAssigned"

    identity_ids = [
      azurerm_user_assigned_identity.main.id,
    ]
  }

  kubelet_identity {
    user_assigned_identity_id = azurerm_user_assigned_identity.main.id
    client_id                 = azurerm_user_assigned_identity.main.client_id
    object_id                 = azurerm_user_assigned_identity.main.principal_id
  }
}
