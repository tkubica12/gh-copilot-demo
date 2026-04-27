"""Prometheus metrics for Toy Service."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Request metrics
http_requests_total = Counter(
    'toy_service_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'toy_service_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Business metrics
toys_registered_total = Counter(
    'toy_service_toys_registered_total',
    'Total number of toys registered'
)

toys_updated_total = Counter(
    'toy_service_toys_updated_total',
    'Total number of toys updated'
)

toys_deleted_total = Counter(
    'toy_service_toys_deleted_total',
    'Total number of toys deleted'
)

avatar_uploads_total = Counter(
    'toy_service_avatar_uploads_total',
    'Total number of avatar uploads'
)

active_toys_gauge = Gauge(
    'toy_service_active_toys',
    'Current number of active toys in the system'
)


async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
