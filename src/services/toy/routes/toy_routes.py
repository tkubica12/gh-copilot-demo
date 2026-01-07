"""Toy API routes."""
import logging
from typing import Annotated, Callable
from uuid import UUID

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from models import Toy, ToyCreate, ToyUpdate
from repositories import ToyRepository
from services import BlobService
from metrics import toys_registered_total, toys_updated_total, toys_deleted_total, avatar_uploads_total

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/toy", tags=["Toy"])

# Dependency injection placeholders (will be set in main.py)
toy_repository: ToyRepository | None = None
blob_service: BlobService | None = None


def get_toy_repo() -> ToyRepository:
    """Dependency to get toy repository instance."""
    if toy_repository is None:
        raise RuntimeError("ToyRepository not initialized")
    return toy_repository


def get_blob_svc() -> BlobService:
    """Dependency to get blob service instance."""
    if blob_service is None:
        raise RuntimeError("BlobService not initialized")
    return blob_service


@router.post("", response_model=Toy, status_code=201)
async def create_toy(
    toy_data: ToyCreate,
    repo: ToyRepository = Depends(get_toy_repo),
) -> Toy:
    """
    Register a new toy.

    If toy_data.id is provided, it will be used; otherwise a new UUID is generated.
    """
    # Create toy, using provided ID if available
    toy_kwargs = {
        "name": toy_data.name.strip(),
        "description": toy_data.description.strip() if toy_data.description else None,
    }
    
    # Only include id if it's provided (let Pydantic auto-generate otherwise)
    if toy_data.id is not None:
        toy_kwargs["id"] = toy_data.id
        
    toy = Toy(**toy_kwargs)

    created_toy = await repo.create(toy)
    toys_registered_total.inc()
    logger.info(f"Created toy {created_toy.id}")

    return created_toy


@router.get("", response_model=dict)
async def list_toys(
    limit: int = 20,
    offset: int = 0,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)] = None,
) -> dict:
    """
    List all toys with pagination.
    """
    toys, total = await repo.list_all(limit=limit, offset=offset)

    # Convert to response format matching OpenAPI spec
    return {"items": [toy.model_dump(mode="json") for toy in toys], "total": total, "limit": limit, "offset": offset}


@router.get("/{toy_id}", response_model=Toy)
async def get_toy(
    toy_id: UUID,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
) -> Toy:
    """Get toy details by ID."""
    toy = await repo.get_by_id(toy_id)
    if not toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    return toy


@router.patch("/{toy_id}", response_model=Toy)
async def update_toy(
    toy_id: UUID,
    toy_update: ToyUpdate,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
) -> Toy:
    """
    Update toy details (partial update).
    """
    # Get existing toy
    toy = await repo.get_by_id(toy_id)
    if not toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    # Apply updates (only non-None fields)
    updates = toy_update.model_dump(exclude_unset=True, exclude_none=True)
    if not updates:
        return toy  # No changes

    updated_toy = await repo.update(toy_id, updates)
    if not updated_toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    toys_updated_total.inc()
    logger.info(f"Updated toy {toy_id}")
    return updated_toy


@router.delete("/{toy_id}", status_code=204)
async def delete_toy(
    toy_id: UUID,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
    blob_svc: Annotated[BlobService, Depends(get_blob_svc)],
):
    """
    Delete a toy.
    """
    # Get existing toy
    toy = await repo.get_by_id(toy_id)
    if not toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    # Delete avatar if exists
    if toy.avatar_blob_name:
        await blob_svc.delete_avatar(toy.avatar_blob_name)

    # Delete toy from database
    deleted = await repo.delete(toy_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Toy not found")

    toys_deleted_total.inc()
    logger.info(f"Deleted toy {toy_id}")


# Avatar endpoints


@router.post("/{toy_id}/avatar", response_model=Toy)
async def upload_avatar(
    toy_id: UUID,
    file: Annotated[UploadFile, File(description="Avatar image (JPEG, PNG, or WebP)")],
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
    blob_svc: Annotated[BlobService, Depends(get_blob_svc)],
) -> Toy:
    """
    Upload avatar image for a toy.
    """
    # Get existing toy
    toy = await repo.get_by_id(toy_id)
    if not toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    try:
        # Delete old avatar if exists
        if toy.avatar_blob_name:
            await blob_svc.delete_avatar(toy.avatar_blob_name)

        # Upload new avatar
        blob_name = await blob_svc.upload_avatar(file, str(toy_id))

        # Update toy with new avatar reference
        updated_toy = await repo.update(toy_id, {"avatar_blob_name": blob_name, "has_avatar": True})

        if not updated_toy:
            raise HTTPException(status_code=404, detail="Toy not found")

        avatar_uploads_total.inc()
        logger.info(f"Uploaded avatar for toy {toy_id}")
        return updated_toy

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to upload avatar: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload avatar")


@router.get("/{toy_id}/avatar")
async def get_avatar(
    toy_id: UUID,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
    blob_svc: Annotated[BlobService, Depends(get_blob_svc)],
) -> StreamingResponse:
    """
    Get avatar image for a toy.

    Streams the image from blob storage.
    """
    # Get toy
    toy = await repo.get_by_id(toy_id)
    if not toy or not toy.avatar_blob_name:
        raise HTTPException(status_code=404, detail="Toy has no avatar image")

    try:
        # Stream avatar from blob storage
        stream, content_type = await blob_svc.stream_avatar(toy.avatar_blob_name)

        return StreamingResponse(
            stream,
            media_type=content_type,
            headers={
                "Cache-Control": "public, max-age=3600",  # 1 hour cache
            },
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Avatar image not found")
    except Exception as e:
        logger.error(f"Failed to retrieve avatar: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve avatar")


@router.delete("/{toy_id}/avatar", status_code=204)
async def delete_avatar(
    toy_id: UUID,
    repo: Annotated[ToyRepository, Depends(get_toy_repo)],
    blob_svc: Annotated[BlobService, Depends(get_blob_svc)],
):
    """
    Delete avatar image for a toy.
    """
    # Get toy
    toy = await repo.get_by_id(toy_id)
    if not toy:
        raise HTTPException(status_code=404, detail="Toy not found")

    if not toy.avatar_blob_name:
        raise HTTPException(status_code=404, detail="Toy has no avatar")

    # Delete avatar from blob storage
    await blob_svc.delete_avatar(toy.avatar_blob_name)

    # Update toy to remove avatar reference
    await repo.update(toy_id, {"avatar_blob_name": None, "has_avatar": False})

    logger.info(f"Deleted avatar for toy {toy_id}")
