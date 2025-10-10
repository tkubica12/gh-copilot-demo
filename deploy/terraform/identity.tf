resource "azurerm_user_assigned_identity" "main" {
  name                = "${local.base_name}-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}