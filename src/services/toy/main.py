"""Main FastAPI application for Toy Service."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from repositories import ToyRepository
from routes import toy_routes
from services import BlobService

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Suppress verbose Azure SDK logging (cosmos, storage, core.pipeline)
logging.getLogger("azure.cosmos").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Global instances
toy_repo: ToyRepository | None = None
blob_svc: BlobService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Initializes and cleans up resources (DB, Blob clients).
    """
    global toy_repo, blob_svc

    logger.info("Starting Toy Service...")

    # Initialize repositories and services
    toy_repo = ToyRepository(
        cosmos_endpoint=settings.cosmos_endpoint,
        database_name=settings.cosmos_database_name,
        container_name=settings.cosmos_container_name,
        credential=settings.cosmos_key,
        disable_ssl_verify=settings.cosmos_disable_ssl_verify,
    )

    blob_svc = BlobService(
        storage_account_url=settings.storage_account_url,
        container_name=settings.blob_container_avatars,
        credential=settings.storage_account_key,
    )

    # Inject into routes module
    toy_routes.toy_repository = toy_repo
    toy_routes.blob_service = blob_svc

    logger.info("Toy Service initialized successfully")

    yield

    # Cleanup
    logger.info("Shutting down Toy Service...")
    if toy_repo:
        await toy_repo.close()
    if blob_svc:
        await blob_svc.close()
    logger.info("Toy Service shut down complete")


# Create FastAPI app
app = FastAPI(
    title="Toy Service",
    description="Toy Registry & Profiles Service for Stuffed Toy World Tour",
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

# Include routers
app.include_router(toy_routes.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "toy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
