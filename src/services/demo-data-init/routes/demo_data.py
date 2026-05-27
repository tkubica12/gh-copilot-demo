"""API endpoints for demo data import orchestration."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Callable

from fastapi import APIRouter, Depends, Header, HTTPException, status

from models import ImportRequest, ImportResponse
from services.importer import DemoDataImportService
from metrics import import_operations_total, toys_imported_total, trips_imported_total, photos_imported_total

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/demo-data", tags=["Demo Data"])

import_service: DemoDataImportService | None = None


def configure_router(*, importer: DemoDataImportService) -> None:
    """Wire up import service singleton (called from main)."""

    global import_service
    import_service = importer
    logger.info("Demo data router configured")


def _get_import_service() -> DemoDataImportService:
    if import_service is None:
        raise HTTPException(status_code=503, detail="Import service not initialized")
    return import_service


@router.post("/import", response_model=ImportResponse, status_code=status.HTTP_200_OK)
async def trigger_import(
    request: ImportRequest,
) -> ImportResponse:
    """Run a synchronous import."""
    try:
        request.ensure_valid()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    importer = _get_import_service()
    started_at = datetime.now(timezone.utc)
    try:
        summary = await importer.import_data(
            include_toys=request.include_toys,
            include_trips=request.include_trips,
        )
        import_operations_total.labels(status="success").inc()
        
        # Track imported items
        toys_imported_total.inc(summary.get("toys_created", 0))
        trips_imported_total.inc(summary.get("trips_created", 0))
        photos_imported_total.inc(summary.get("photos_uploaded", 0))
        
    except Exception as exc:  # pragma: no cover - surfaced as HTTP error
        import_operations_total.labels(status="failure").inc()
        logger.exception("Demo data import failed")
        raise HTTPException(status_code=502, detail="Demo data import failed") from exc

    duration_ms = int((datetime.now(timezone.utc) - started_at).total_seconds() * 1000)
    return ImportResponse(
        include_toys=request.include_toys,
        include_trips=request.include_trips,
        summary=summary,
        duration_ms=duration_ms,
    )
