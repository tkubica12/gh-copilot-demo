terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4"
    }
  }
}

provider "azurerm" {
  subscription_id = "673af34d-6b28-41dc-bc7b-f507418045e6"
  features {}
}

