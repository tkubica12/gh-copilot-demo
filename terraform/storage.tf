resource "azurerm_storage_account" "main" {
  name                            = "st${local.base_name_nodash}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  default_to_oauth_authentication = true
  local_user_enabled              = false
}

resource "azurerm_storage_container" "main" {
  name               = "data"
  storage_account_id = azurerm_storage_account.main.id
}
