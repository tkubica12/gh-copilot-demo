"""Trip API routes."""
import logging
from typing import Annotated, Callable
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, Query
from fastapi.responses import StreamingResponse
import httpx

from models import Trip, TripCreate, TripUpdate, GalleryImage
from repositories import TripRepository
from services import GalleryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trip", tags=["Trip"])

# Dependency injection placeholders (will be set in main.py)
trip_repository: TripRepository | None = None
gallery_service: GalleryService | None = None
toy_service_url: str | None = None


def set_toy_service_url(url: str):
    """Set the toy service URL for inter-service calls."""
    global toy_service_url
    toy_service_url = url
    logger.info(f"Toy service URL set to: {url}")


def get_trip_repo() -> TripRepository:
    """Dependency to get trip repository instance."""
    if trip_repository is None:
        raise RuntimeError("TripRepository not initialized")
    return trip_repository


def get_gallery_svc() -> GalleryService:
    """Dependency to get gallery service instance."""
    if gallery_service is None:
        raise RuntimeError("GalleryService not initialized")
    return gallery_service


@router.post("", response_model=Trip, status_code=201)
async def create_trip(
    trip_data: TripCreate,
    repo: TripRepository = Depends(get_trip_repo),
) -> Trip:
    """
    Create a new trip for a toy.
    """
    # Create trip
    trip_kwargs = {
        "title": trip_data.title.strip(),
        "description": trip_data.description.strip() if trip_data.description else None,
        "location_name": trip_data.location_name.strip(),
        "country_code": trip_data.country_code,
        "toy_id": trip_data.toy_id,
        "public_tracking_enabled": trip_data.public_tracking_enabled,
    }
    if trip_data.id is not None:
        trip_kwargs["id"] = trip_data.id

    trip = Trip(**trip_kwargs)

    created_trip = await repo.create(trip)
    logger.info(f"Created trip {created_trip.id} for toy {trip_data.toy_id}")

    return created_trip


@router.get("/{trip_id}", response_model=Trip)
async def get_trip(
    trip_id: UUID,
    repo: TripRepository = Depends(get_trip_repo),
) -> Trip:
    """
    Get trip details including gallery.

    Global read access.
    """
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    logger.debug(f"Retrieved trip {trip_id}")
    return trip


@router.get("", response_model=dict)
async def list_trips(
    repo: TripRepository = Depends(get_trip_repo),
    toy_id: UUID | None = Query(None, description="Filter by toy ID"),
    limit: int = Query(20, ge=1, le=1000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> dict:
    """
    List trips with optional filtering.

    Global read access.
    """
    if toy_id:
        trips, total = await repo.list_by_toy(toy_id, limit, offset)
    else:
        # For now, require at least one filter to prevent full table scan
        raise HTTPException(status_code=400, detail="Must specify toy_id filter")

    logger.debug(f"Listed {len(trips)} trips (total: {total})")

    return {
        "items": trips,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.patch("/{trip_id}", response_model=Trip)
async def update_trip(
    trip_id: UUID,
    trip_update: TripUpdate,
    repo: TripRepository = Depends(get_trip_repo),
) -> Trip:
    """
    Update trip details.
    """
    # Get existing trip
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Apply updates (only non-None fields)
    updates = trip_update.model_dump(exclude_unset=True, exclude_none=True)
    if not updates:
        return trip  # No changes

    updated_trip = await repo.update(trip_id, updates)
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    logger.info(f"Updated trip {trip_id}")
    return updated_trip


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(
    trip_id: UUID,
    repo: Annotated[TripRepository, Depends(get_trip_repo)],
    gallery_svc: Annotated[GalleryService, Depends(get_gallery_svc)],
):
    """
    Delete a trip.
    """
    # Get existing trip
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Delete all gallery images
    for image in trip.gallery:
        await gallery_svc.delete_image(image.blob_name)

    # Delete trip from database
    deleted = await repo.delete(trip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trip not found")

    logger.info(f"Deleted trip {trip_id}")


# Gallery endpoints


@router.post("/{trip_id}/gallery", response_model=Trip)
async def upload_gallery_image(
    trip_id: UUID,
    landmark: str | None = Query(None, max_length=200, description="Optional landmark name"),
    caption: str | None = Query(None, max_length=500, description="Optional image caption"),
    file: UploadFile = File(..., description="Gallery image (JPEG, PNG, or WebP)"),
    repo: TripRepository = Depends(get_trip_repo),
    gallery_svc: GalleryService = Depends(get_gallery_svc),
) -> Trip:
    """
    Upload a gallery image for a trip.

    Can optionally associate with a landmark.
    """
    # Get existing trip
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    try:
        # Upload image to blob storage
        blob_name = await gallery_svc.upload_image(file, str(trip_id))

        # Create gallery image metadata
        image = GalleryImage(
            landmark=landmark,
            blob_name=blob_name,
            caption=caption,
            source="user",
        )

        # Add to trip gallery
        updated_trip = await repo.add_gallery_image(trip_id, image)
        if not updated_trip:
            raise HTTPException(status_code=404, detail="Trip not found")

        logger.info(f"Uploaded gallery image for trip {trip_id}, landmark {landmark}")
        return updated_trip

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to upload gallery image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload gallery image")


@router.get("/{trip_id}/gallery/{image_id}")
async def get_gallery_image(
    trip_id: UUID,
    image_id: UUID,
    repo: TripRepository = Depends(get_trip_repo),
    gallery_svc: GalleryService = Depends(get_gallery_svc),
):
    """
    Download a gallery image.

    Global read access.
    """
    # Get trip to verify image exists
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Find image in gallery
    image = next((img for img in trip.gallery if str(img.image_id) == str(image_id)), None)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found in gallery")

    try:
        # Stream image from blob storage
        stream, content_type = await gallery_svc.stream_image(image.blob_name)

        return StreamingResponse(
            stream,
            media_type=content_type,
            headers={
                "Cache-Control": "public, max-age=3600",  # 1 hour cache
                "Content-Disposition": f'inline; filename="gallery-{image_id}.jpg"',
            },
        )

    except FileNotFoundError:
        logger.error(f"Blob not found for image {image_id}: {image.blob_name}")
        raise HTTPException(status_code=404, detail="Image file not found")
    except Exception as e:
        logger.error(f"Failed to retrieve gallery image: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve image")


@router.delete("/{trip_id}/gallery/{image_id}", status_code=204)
async def delete_gallery_image(
    trip_id: UUID,
    image_id: UUID,
    repo: Annotated[TripRepository, Depends(get_trip_repo)],
    gallery_svc: Annotated[GalleryService, Depends(get_gallery_svc)],
):
    """
    Delete a gallery image.
    """
    # Get existing trip
    trip = await repo.get_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Find image in gallery
    image = next((img for img in trip.gallery if str(img.image_id) == str(image_id)), None)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found in gallery")

    # Delete blob from storage
    await gallery_svc.delete_image(image.blob_name)

    # Remove from trip gallery
    updated_trip = await repo.remove_gallery_image(trip_id, image_id)
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    logger.info(f"Deleted gallery image {image_id} from trip {trip_id}")



