#!/bin/sh
set -e

# Generate env-config.js from environment variables
cat > /usr/share/nginx/html/env-config.js <<EOF
window.ENV_CONFIG = {
  TOY_SERVICE_URL: '${TOY_SERVICE_URL:-http://localhost:8001}',
  TRIP_SERVICE_URL: '${TRIP_SERVICE_URL:-http://localhost:8002}',
  DEMO_DATA_API_URL: '${DEMO_DATA_API_URL:-http://localhost:8010}',
};
EOF

echo "Generated env-config.js with:"
echo "  TOY_SERVICE_URL: ${TOY_SERVICE_URL:-http://localhost:8001}"
echo "  TRIP_SERVICE_URL: ${TRIP_SERVICE_URL:-http://localhost:8002}"
echo "  DEMO_DATA_API_URL: ${DEMO_DATA_API_URL:-http://localhost:8010}"

# Execute the main container command (nginx)
exec "$@"
