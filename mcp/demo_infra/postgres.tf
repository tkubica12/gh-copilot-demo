resource "random_string" "postgres" {
  length  = 8
  special = false
  upper   = false
  numeric = true
  lower   = true
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-${local.base_name}-${random_string.postgres.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  administrator_login    = "psqladmin"
  administrator_password = random_string.postgres_password.result

  sku_name   = "B_Standard_B1ms"
  storage_mb = 32768
  version    = "16"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  public_network_access_enabled = true
}

resource "random_string" "postgres_password" {
  length  = 24
  special = true
  upper   = true
  numeric = true
  lower   = true
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_all" {
  name             = "AllowAll"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

output "postgres_server_name" {
  value       = azurerm_postgresql_flexible_server.main.name
  description = "PostgreSQL Flexible Server name"
}

output "postgres_fqdn" {
  value       = azurerm_postgresql_flexible_server.main.fqdn
  description = "PostgreSQL Flexible Server FQDN"
}

output "postgres_admin_login" {
  value       = azurerm_postgresql_flexible_server.main.administrator_login
  description = "PostgreSQL administrator login"
}

output "postgres_admin_password" {
  value       = random_string.postgres_password.result
  sensitive   = true
  description = "PostgreSQL administrator password"
}
