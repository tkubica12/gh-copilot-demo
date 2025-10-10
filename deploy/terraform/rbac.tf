// Storage
resource "azurerm_role_assignment" "self_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "app_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azurerm_role_assignment" "self_controlplane_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Queue Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "self_servicebus_sender" {
  scope                = azurerm_servicebus_namespace.main.id
  role_definition_name = "Azure Service Bus Data Sender"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "app_servicebus_sender" {
  scope                = azurerm_servicebus_namespace.main.id
  role_definition_name = "Azure Service Bus Data Sender"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azurerm_role_assignment" "self_servicebus_receiver" {
  scope                = azurerm_servicebus_namespace.main.id
  role_definition_name = "Azure Service Bus Data Receiver"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "app_servicebus_receiver" {
  scope                = azurerm_servicebus_namespace.main.id
  role_definition_name = "Azure Service Bus Data Receiver"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

// Cosmos DB
resource "random_uuid" "cosmosdb_role_assignment_guid_self" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_app" {}

resource "azurerm_cosmosdb_sql_role_definition" "main" {
  name                = "mywriter"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  type                = "CustomRole"
  assignable_scopes   = [azurerm_cosmosdb_account.main.id]

  permissions {
    data_actions = [
      "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
      "Microsoft.DocumentDB/databaseAccounts/readMetadata"
    ]
  }
}

resource "azurerm_cosmosdb_sql_role_assignment" "self" {
  name                = random_uuid.cosmosdb_role_assignment_guid_self.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = data.azurerm_client_config.current.object_id
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "app" {
  name                = random_uuid.cosmosdb_role_assignment_guid_app.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azurerm_user_assigned_identity.main.principal_id
  scope               = azurerm_cosmosdb_account.main.id
}
