"""Blob storage service for gallery images.

This module uses the async Azure Blob Storage SDK (azure.storage.blob.aio) which
is designed for use with async frameworks like FastAPI. The async SDK provides
native async/await support without blocking the event loop.
"""
import logging
import mimetypes
from io import BytesIO
from uuid import uuid4

from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings
from azure.core.exceptions import ServiceRequestError, ClientAuthenticationError  # type: ignore
from fastapi import UploadFile

from typing import Any

logger = logging.getLogger(__name__)


class GalleryService:
    """Service for managing gallery image blob storage operations."""

    # Supported image formats
    ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB (larger than avatars for high-quality trip photos)

    def __init__(self, storage_account_url: str, container_name: str, credential: Any = None):
        """
        Initialize gallery service.

        Args:
            storage_account_url: Storage account URL
            container_name: Container name for gallery images
            credential: Optional credential (key or TokenCredential)
        """
        self.storage_account_url = storage_account_url
        self.container_name = container_name
        self.credential = credential
        self._client: BlobServiceClient | None = None
        self._container_client = None

    async def _ensure_initialized(self):
        """Ensure blob service client and container are initialized."""
        if self._container_client is not None:
            return

        # Initialize async client
        if self.credential:
            self._client = BlobServiceClient(account_url=self.storage_account_url, credential=self.credential)
        else:
            # Initialize async client with managed identity
            # Exclude shared token cache to prevent home tenant confusion in multi-tenant scenarios
            # Local: Uses Azure CLI (logged in with correct tenant)
            # AKS: Uses Workload Identity / Managed Identity (federated identity)
            credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
            self._client = BlobServiceClient(account_url=self.storage_account_url, credential=credential)

        # Get container and create if it doesn't exist (for local development with emulator)
        self._container_client = self._client.get_container_client(self.container_name)
        try:
            await self._container_client.create_container()
            logger.info(f"Created container '{self.container_name}'")
        except Exception:
            # Container already exists, which is fine
            pass
        logger.info(f"Connected to container '{self.container_name}'")

    async def upload_image(self, file: UploadFile, trip_id: str) -> str:
        """
        Upload gallery image to blob storage.

        Args:
            file: Uploaded file from FastAPI
            trip_id: Trip ID for organizing blobs

        Returns:
            Blob name (reference for database)

        Raises:
            ValueError: If file type or size is invalid
        """
        await self._ensure_initialized()

        # Validate content type
        content_type = file.content_type
        if content_type not in self.ALLOWED_CONTENT_TYPES:
            raise ValueError(
                f"Unsupported file type: {content_type}. Allowed: {', '.join(self.ALLOWED_CONTENT_TYPES)}"
            )

        # Read file content and validate size
        content = await file.read()
        if len(content) > self.MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds maximum of {self.MAX_FILE_SIZE_BYTES / 1024 / 1024}MB")

        # Generate blob name: {trip_id}/{uuid}.{extension}
        extension = mimetypes.guess_extension(content_type) or ".jpg"
        blob_name = f"{trip_id}/{uuid4()}{extension}"

        # Upload to blob storage
        blob_client = self._container_client.get_blob_client(blob_name)
        content_settings = ContentSettings(content_type=content_type)

        try:
            await blob_client.upload_blob(
                data=content,
                content_settings=content_settings,
                overwrite=True,
            )
        except (ServiceRequestError, ClientAuthenticationError, TimeoutError) as e:  # network / auth layer
            logger.error(f"Failed to upload gallery image (network/auth): {e}")
            raise ValueError("Gallery image upload failed due to storage connectivity or authentication issue") from e
        except Exception as e:  # pragma: no cover - unexpected
            logger.error(f"Unexpected failure uploading gallery image: {e}")
            raise ValueError("Unexpected error uploading gallery image") from e

        logger.info(f"Uploaded gallery image: {blob_name} ({len(content)} bytes)")
        return blob_name

    async def download_image(self, blob_name: str) -> tuple[bytes, str]:
        """
        Download gallery image from blob storage.

        Args:
            blob_name: Blob reference from database

        Returns:
            Tuple of (image bytes, content type)

        Raises:
            FileNotFoundError: If blob doesn't exist
        """
        await self._ensure_initialized()

        blob_client = self._container_client.get_blob_client(blob_name)

        try:
            download_stream = await blob_client.download_blob()
            content = await download_stream.readall()
            properties = await blob_client.get_blob_properties()
            content_type = properties.content_settings.content_type or "application/octet-stream"

            logger.debug(f"Downloaded gallery image: {blob_name} ({len(content)} bytes)")
            return content, content_type
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to download blob {blob_name}: {e}")
            raise FileNotFoundError(f"Gallery image not found: {blob_name}") from e

    async def delete_image(self, blob_name: str) -> bool:
        """
        Delete gallery image from blob storage.

        Args:
            blob_name: Blob reference from database

        Returns:
            True if deleted, False if not found
        """
        await self._ensure_initialized()

        blob_client = self._container_client.get_blob_client(blob_name)

        try:
            await blob_client.delete_blob()
            logger.info(f"Deleted gallery image: {blob_name}")
            return True
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Failed to delete blob {blob_name}: {e}")
            return False

    async def stream_image(self, blob_name: str) -> tuple[BytesIO, str]:
        """
        Stream gallery image from blob storage (memory efficient).

        Args:
            blob_name: Blob reference from database

        Returns:
            Tuple of (BytesIO stream, content type)

        Raises:
            FileNotFoundError: If blob doesn't exist
        """
        content, content_type = await self.download_image(blob_name)
        return BytesIO(content), content_type

    async def close(self):
        """Close blob service client connection."""
        if self._client:
            await self._client.close()
            logger.info("Gallery service client closed")
