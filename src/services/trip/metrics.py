"""Prometheus metrics for Trip Service."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Request metrics
http_requests_total = Counter(
    'trip_service_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'trip_service_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Business metrics
trips_created_total = Counter(
    'trip_service_trips_created_total',
    'Total number of trips created'
)

trips_updated_total = Counter(
    'trip_service_trips_updated_total',
    'Total number of trips updated'
)

trips_deleted_total = Counter(
    'trip_service_trips_deleted_total',
    'Total number of trips deleted'
)

photos_uploaded_total = Counter(
    'trip_service_photos_uploaded_total',
    'Total number of photos uploaded'
)

active_trips_gauge = Gauge(
    'trip_service_active_trips',
    'Current number of active trips'
)


async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
