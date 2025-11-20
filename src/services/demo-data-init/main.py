"""Entry point for the demo data init FastAPI service."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import configure_router, router
from services.importer import DemoDataImportService

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting demo data init service")
    importer = DemoDataImportService(
        assets_path=settings.assets_path,
        toy_service_url=settings.toy_service_url,
        trip_service_url=settings.trip_service_url,
        http_timeout=settings.http_timeout_seconds,
        max_retries=settings.max_retry_attempts,
    )

    configure_router(
        importer=importer,
    )

    logger.info("Demo data init service ready")
    try:
        yield
    finally:
        logger.info("Shutting down demo data init service")
        logger.info("Shutdown complete")


app = FastAPI(
    title="Demo Data Init",
    description="Admin-only service to reseed demo datasets",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "demo-data-init"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
