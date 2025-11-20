// Runtime configuration that can be replaced in Docker container
// This file is loaded before the app bundle and provides runtime config via window.ENV_CONFIG
window.ENV_CONFIG = {
  TOY_SERVICE_URL: 'http://localhost:8001',
  TRIP_SERVICE_URL: 'http://localhost:8002',
  DEMO_DATA_API_URL: 'http://localhost:8010',
};
