resource "azurerm_storage_account" "main" {
  name                            = "tomaskubicastorageacc"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = true
  https_traffic_only_enabled      = false
  min_tls_version                 = "TLS1_0"
  public_network_access_enabled   = true
  local_user_enabled              = true
  shared_access_key_enabled       = true
}
