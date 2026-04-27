"""Main FastAPI application for Trip Service."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from repositories import TripRepository
from routes import trip_routes
from services import GalleryService
from middleware import MetricsMiddleware
from metrics import metrics_endpoint

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Suppress verbose Azure SDK logging
logging.getLogger("azure.cosmos").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Global instances
trip_repo: TripRepository | None = None
gallery_svc: GalleryService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Initializes and cleans up resources (DB, Blob clients).
    """
    global trip_repo, gallery_svc

    logger.info("Starting Trip Service...")

    # Initialize repositories and services
    trip_repo = TripRepository(
        cosmos_endpoint=settings.cosmos_endpoint,
        database_name=settings.cosmos_database_name,
        container_name=settings.cosmos_container_name,
        credential=settings.cosmos_key,
        disable_ssl_verify=settings.cosmos_disable_ssl_verify,
    )

    gallery_svc = GalleryService(
        storage_account_url=settings.storage_account_url,
        container_name=settings.blob_container_gallery,
        credential=settings.storage_account_key,
    )

    # Inject into routes module
    trip_routes.trip_repository = trip_repo
    trip_routes.gallery_service = gallery_svc
    trip_routes.set_toy_service_url(settings.toy_service_url)

    logger.info("Trip Service initialized successfully")

    yield

    # Cleanup
    logger.info("Shutting down Trip Service...")
    if trip_repo:
        await trip_repo.close()
    if gallery_svc:
        await gallery_svc.close()
    logger.info("Trip Service shut down complete")


# Create FastAPI app
app = FastAPI(
    title="Trip Service",
    description="Trip & Gallery Service for Stuffed Toy World Tour",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware (configure as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics middleware
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(trip_routes.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "trip"}


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return await metrics_endpoint()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
        log_level=settings.log_level.lower(),
    )
