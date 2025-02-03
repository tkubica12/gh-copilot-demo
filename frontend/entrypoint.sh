#!/bin/sh

# ...existing code...
envsubst '$REACT_APP_PROCESS_API_URL' < /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.html.tmp \
  && mv /usr/share/nginx/html/index.html.tmp /usr/share/nginx/html/index.html

exec "$@"
