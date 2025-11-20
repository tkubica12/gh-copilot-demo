"""HTTP-based importer that reseeds demo data via downstream services."""
from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Iterable

import httpx
from tenacity import AsyncRetrying, stop_after_attempt, wait_random_exponential

from models import OperationSummary

logger = logging.getLogger(__name__)


class DemoDataImportService:
    """Implementation that calls the toy & trip services using the caller token."""

    def __init__(
        self,
        *,
        assets_path: Path,
        toy_service_url: str,
        trip_service_url: str,
        http_timeout: int,
        max_retries: int,
    ) -> None:
        self.assets_path = assets_path
        self.toy_service_url = toy_service_url.rstrip("/")
        self.trip_service_url = trip_service_url.rstrip("/")
        self.http_timeout = http_timeout
        self.max_retries = max_retries
        self.toy_profiles_path = assets_path / "toy_profiles.json"
        self.trips_path = assets_path / "trips.json"
        self.toy_images_path = assets_path / "toy-images"
        self.trip_images_path = assets_path / "trip-images"

    async def import_data(self, *, include_toys: bool, include_trips: bool) -> OperationSummary:
        """Reseed demo data using downstream service APIs."""

        summary = OperationSummary()
        headers = {}

        async with httpx.AsyncClient(timeout=self.http_timeout) as client:
            if include_toys:
                await self._import_toys(client, headers, summary)
            if include_trips:
                await self._import_trips(client, headers, summary)
        return summary

    async def _import_toys(
        self,
        client: httpx.AsyncClient,
        headers: dict[str, str],
        summary: OperationSummary,
    ) -> None:
        profiles = self._load_json_list(self.toy_profiles_path)
        for profile in profiles:
            toy_id = profile.get("id")
            if not toy_id:
                logger.warning("Skipping toy profile without id: %s", profile)
                summary.toy_failures += 1
                continue

            await self._delete_existing(client, f"{self.toy_service_url}/toy/{toy_id}", headers)

            payload = {
                "id": toy_id,
                "name": profile.get("name"),
                "description": profile.get("description", ""),
            }

            try:
                response = await self._request_with_retry(
                    client,
                    "POST",
                    f"{self.toy_service_url}/toy",
                    json=payload,
                    headers=headers,
                )
                if response.status_code not in (200, 201):
                    logger.error("Toy create failed (%s): %s", response.status_code, response.text)
                    summary.toy_failures += 1
                    continue
                summary.toys_processed += 1
            except Exception:
                logger.exception("Creating toy %s failed", toy_id)
                summary.toy_failures += 1
                continue

            avatar_name = profile.get("avatar_blob_name")
            if avatar_name:
                uploaded = await self._upload_avatar(client, toy_id, avatar_name, headers)
                if uploaded:
                    summary.toy_avatars_uploaded += 1

    async def _import_trips(
        self,
        client: httpx.AsyncClient,
        headers: dict[str, str],
        summary: OperationSummary,
    ) -> None:
        trips = self._load_json_list(self.trips_path)
        for record in trips:
            trip_id = record.get("trip_id")
            toy_id = record.get("toy_id")
            if not toy_id:
                logger.warning("Skipping trip without toy reference: %s", record)
                summary.trip_failures += 1
                continue

            if trip_id:
                await self._delete_existing(client, f"{self.trip_service_url}/trip/{trip_id}", headers)

            payload: dict[str, Any] = {
                "title": record.get("title"),
                "description": record.get("description", ""),
                "location_name": record.get("location_name"),
                "country_code": record.get("country_code", "US"),
                "toy_id": toy_id,
                "public_tracking_enabled": True,
            }
            if trip_id:
                payload["id"] = trip_id

            try:
                response = await self._request_with_retry(
                    client,
                    "POST",
                    f"{self.trip_service_url}/trip",
                    json=payload,
                    headers=headers,
                )
                if response.status_code not in (200, 201):
                    logger.error("Trip create failed (%s): %s", response.status_code, response.text)
                    summary.trip_failures += 1
                    continue
                created_trip = response.json()
                summary.trips_processed += 1
                await self._sync_trip_gallery(
                    client,
                    created_trip["id"],
                    record.get("gallery_images", []),
                    headers,
                    summary,
                )
            except Exception:
                logger.exception("Creating trip failed for toy %s", toy_id)
                summary.trip_failures += 1

    async def _upload_avatar(
        self,
        client: httpx.AsyncClient,
        toy_id: str,
        avatar_blob: str,
        headers: dict[str, str],
    ) -> bool:
        image_path = self.toy_images_path / avatar_blob
        if not image_path.exists():
            logger.warning("Avatar image missing: %s", avatar_blob)
            return False

        file_content = await asyncio.to_thread(image_path.read_bytes)
        files = {"file": (avatar_blob, file_content, "image/jpeg")}
        form_headers = {}
        try:
            response = await self._request_with_retry(
                client,
                "POST",
                f"{self.toy_service_url}/toy/{toy_id}/avatar",
                headers=form_headers,
                files=files,
            )
            if response.status_code not in (200, 201):
                logger.error("Avatar upload failed (%s): %s", response.status_code, response.text)
                return False
            return True
        except Exception:
            logger.exception("Avatar upload failed for toy %s", toy_id)
            return False

    async def _sync_trip_gallery(
        self,
        client: httpx.AsyncClient,
        trip_id: str,
        gallery: Iterable[dict[str, Any]],
        headers: dict[str, str],
        summary: OperationSummary,
    ) -> None:
        for image in gallery:
            blob_name = image.get("blob_name")
            if not blob_name:
                continue
            image_path = self.trip_images_path / blob_name
            if not image_path.exists():
                logger.warning("Gallery image missing: %s", blob_name)
                continue

            file_bytes = await asyncio.to_thread(image_path.read_bytes)
            params = {
                "landmark": image.get("landmark"),
                "caption": image.get("caption"),
            }
            files = {"file": (blob_name, file_bytes, "image/jpeg")}
            response = await self._request_with_retry(
                client,
                "POST",
                f"{self.trip_service_url}/trip/{trip_id}/gallery",
                headers=headers,
                params={k: v for k, v in params.items() if v},
                files=files,
            )
            if response.status_code not in (200, 201):
                logger.error("Gallery upload failed for trip %s (%s): %s", trip_id, blob_name, response.text)
                continue
            summary.images_uploaded += 1

    async def _delete_existing(self, client: httpx.AsyncClient, url: str, headers: dict[str, str]) -> None:
        try:
            response = await client.delete(url, headers=headers)
            if response.status_code in (204, 404):
                return
            if response.status_code == 403:
                logger.warning("Forbidden deleting %s", url)
        except httpx.RequestError as exc:
            logger.warning("Delete %s failed: %s", url, exc)

    async def _request_with_retry(self, client: httpx.AsyncClient, method: str, url: str, **kwargs) -> httpx.Response:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_random_exponential(multiplier=0.5, max=5),
            reraise=True,
        ):
            with attempt:
                response = await client.request(method, url, **kwargs)
                if response.status_code >= 500:
                    response.raise_for_status()
                return response

    def _load_json_list(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset file: {path}")
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError(f"Expected list in {path}")
        return data
