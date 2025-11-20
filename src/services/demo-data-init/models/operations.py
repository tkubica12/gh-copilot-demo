"""Schemas describing import operations."""
from __future__ import annotations

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    """Request body for triggering a demo data import."""

    include_toys: bool = Field(True, description="Whether toy profiles should be reseeded")
    include_trips: bool = Field(True, description="Whether trip itineraries should be reseeded")

    def ensure_valid(self) -> None:
        """Validate that at least one dataset is requested."""
        if not self.include_toys and not self.include_trips:
            raise ValueError("At least one dataset (toys or trips) must be selected")


class OperationSummary(BaseModel):
    """Processing stats returned in the status endpoint."""

    toys_processed: int = 0
    toy_failures: int = 0
    toy_avatars_uploaded: int = 0
    trips_processed: int = 0
    trip_failures: int = 0
    images_uploaded: int = 0


class ImportResponse(BaseModel):
    """Synchronous response returned after running an import."""

    include_toys: bool
    include_trips: bool
    summary: OperationSummary
    duration_ms: int = Field(..., ge=0, description="Total runtime in milliseconds")
