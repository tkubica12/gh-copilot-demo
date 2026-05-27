"""Prometheus metrics for Demo Data Init Service."""
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Request metrics
http_requests_total = Counter(
    'demo_data_init_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'demo_data_init_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Business metrics
import_operations_total = Counter(
    'demo_data_init_import_operations_total',
    'Total number of import operations',
    ['status']  # success, failure
)

toys_imported_total = Counter(
    'demo_data_init_toys_imported_total',
    'Total number of toys imported'
)

trips_imported_total = Counter(
    'demo_data_init_trips_imported_total',
    'Total number of trips imported'
)

photos_imported_total = Counter(
    'demo_data_init_photos_imported_total',
    'Total number of photos imported'
)


async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
