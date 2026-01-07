# Import Grafana dashboards using local files
# Note: This requires the Grafana provider to be configured

resource "grafana_dashboard" "toy_service" {
  config_json = file("${path.module}/../../deploy/grafana/dashboards/toy-service-dashboard.json")
  
  depends_on = [azurerm_dashboard_grafana.main]
}

resource "grafana_dashboard" "trip_service" {
  config_json = file("${path.module}/../../deploy/grafana/dashboards/trip-service-dashboard.json")
  
  depends_on = [azurerm_dashboard_grafana.main]
}

resource "grafana_dashboard" "demo_data_init" {
  config_json = file("${path.module}/../../deploy/grafana/dashboards/demo-data-init-dashboard.json")
  
  depends_on = [azurerm_dashboard_grafana.main]
}
