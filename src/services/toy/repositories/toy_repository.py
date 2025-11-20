"""Repository for toy data access in Cosmos DB.

This module uses the async Azure Cosmos SDK (azure.cosmos.aio) which is designed
for use with async frameworks like FastAPI. The async SDK provides native async/await
support without blocking the event loop.
"""
import logging
from typing import Any
from uuid import UUID

from azure.cosmos.aio import ContainerProxy, CosmosClient, DatabaseProxy
from azure.cosmos import PartitionKey, exceptions
from azure.identity.aio import DefaultAzureCredential

from models import Toy, ToyDocument

logger = logging.getLogger(__name__)


class ToyRepository:
    """Repository for toy CRUD operations in Cosmos DB."""

    def __init__(self, cosmos_endpoint: str, database_name: str, container_name: str, credential: Any = None, disable_ssl_verify: bool = False):
        """
        Initialize the toy repository.

        Args:
            cosmos_endpoint: Cosmos DB account endpoint URL
            database_name: Name of the database
            container_name: Name of the container (collection)
            credential: Optional credential (key or TokenCredential)
            disable_ssl_verify: Whether to disable SSL certificate verification
        """
        self.cosmos_endpoint = cosmos_endpoint
        self.database_name = database_name
        self.container_name = container_name
        self.credential = credential
        self.disable_ssl_verify = disable_ssl_verify
        self._client: CosmosClient | None = None
        self._database: DatabaseProxy | None = None
        self._container: ContainerProxy | None = None

    async def _ensure_initialized(self) -> ContainerProxy:
        """
        Ensure Cosmos client, database, and container are initialized.

        Returns:
            ContainerProxy instance ready for operations
        """
        if self._container is not None:
            return self._container

        # Initialize async client
        if self.credential:
            # Use provided credential (e.g. key for emulator)
            # When using emulator, disable SSL verify and endpoint discovery to avoid internal IP redirection
            self._client = CosmosClient(
                self.cosmos_endpoint, 
                credential=self.credential,
                connection_verify=not self.disable_ssl_verify,
                enable_endpoint_discovery=not self.disable_ssl_verify
            )
        else:
            # Initialize async client with managed identity
            # Exclude shared token cache to prevent home tenant confusion in multi-tenant scenarios
            # Local: Uses Azure CLI (logged in with correct tenant)
            # AKS: Uses Workload Identity / Managed Identity (federated identity)
            credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
            self._client = CosmosClient(
                self.cosmos_endpoint, 
                credential=credential,
                connection_verify=not self.disable_ssl_verify,
                enable_endpoint_discovery=not self.disable_ssl_verify
            )

        # Get existing database (created via Bicep)
        if self.disable_ssl_verify:
            # Local development with emulator: create resources if they don't exist
            try:
                self._database = await self._client.create_database_if_not_exists(id=self.database_name)
                self._container = await self._database.create_container_if_not_exists(
                    id=self.container_name, 
                    partition_key=PartitionKey(path="/id")
                )
            except Exception as e:
                # If creation fails, try to get existing
                logger.warning(f"Could not create database/container, attempting to get existing: {e}")
                self._database = self._client.get_database_client(self.database_name)
                self._container = self._database.get_container_client(self.container_name)
        else:
            self._database = self._client.get_database_client(self.database_name)
            self._container = self._database.get_container_client(self.container_name)

        logger.info(f"Connected to database '{self.database_name}' and container '{self.container_name}'")

        return self._container

    async def create(self, toy: Toy) -> Toy:
        """
        Create a new toy in the database.

        Args:
            toy: Toy instance to create

        Returns:
            Created Toy with server-assigned timestamps

        Raises:
            exceptions.CosmosResourceExistsError: If toy with same ID already exists
        """
        container = await self._ensure_initialized()
        doc = ToyDocument.from_toy(toy)
        item = doc.model_dump(by_alias=False, mode="json")

        # Cosmos DB needs both "id" (document ID) and "toy_id" (partition key)
        # They should have the same value
        item["id"] = str(toy.id)
        item["toy_id"] = str(toy.id)

        created_item = await container.create_item(body=item)
        logger.info(f"Created toy: {created_item['id']}")

        return ToyDocument(**created_item).to_toy()

    async def get_by_id(self, toy_id: UUID) -> Toy | None:
        """
        Retrieve a toy by ID.

        Args:
            toy_id: UUID of the toy

        Returns:
            Toy if found, None otherwise
        """
        container = await self._ensure_initialized()
        toy_id_str = str(toy_id)

        try:
            item = await container.read_item(item=toy_id_str, partition_key=toy_id_str)
            return ToyDocument(**item).to_toy()
        except exceptions.CosmosResourceNotFoundError:
            logger.debug(f"Toy not found: {toy_id_str}")
            return None

    async def list_all(self, limit: int = 20, offset: int = 0) -> tuple[list[Toy], int]:
        """
        List toys with pagination.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip

        Returns:
            Tuple of (list of toys, total count)
        """
        container = await self._ensure_initialized()

        # Build query
        # Note: Async client automatically handles cross-partition queries - no enable_cross_partition_query flag needed
        query = "SELECT * FROM c ORDER BY c.created_at DESC"
        items = [item async for item in container.query_items(
            query=query,
        )]
        
        total = len(items)
        paginated_items = items[offset : offset + limit]

        toys = [ToyDocument(**item).to_toy() for item in paginated_items]
        logger.debug(f"Listed {len(toys)} toys (total: {total})")

        return toys, total

    async def update(self, toy_id: UUID, updates: dict[str, Any]) -> Toy | None:
        """
        Update a toy with partial data.

        Args:
            toy_id: UUID of the toy to update
            updates: Dictionary of fields to update

        Returns:
            Updated Toy if found, None otherwise
        """
        container = await self._ensure_initialized()
        toy_id_str = str(toy_id)

        try:
            # Read current item
            item = await container.read_item(item=toy_id_str, partition_key=toy_id_str)

            # Apply updates
            for key, value in updates.items():
                if key not in {"id", "toy_id", "created_at"}:  # Immutable fields
                    item[key] = value

            # Update timestamp
            from datetime import datetime, UTC

            item["updated_at"] = datetime.now(UTC).isoformat()

            # Replace item
            updated_item = await container.replace_item(item=item, body=item)
            logger.info(f"Updated toy: {toy_id_str}")
            return ToyDocument(**updated_item).to_toy()

        except exceptions.CosmosResourceNotFoundError:
            logger.debug(f"Toy not found for update: {toy_id_str}")
            return None

    async def delete(self, toy_id: UUID) -> bool:
        """
        Delete a toy.

        Args:
            toy_id: UUID of the toy to delete

        Returns:
            True if deleted, False if not found
        """
        container = await self._ensure_initialized()
        toy_id_str = str(toy_id)

        try:
            await container.delete_item(item=toy_id_str, partition_key=toy_id_str)
            logger.info(f"Deleted toy: {toy_id_str}")
            return True
        except exceptions.CosmosResourceNotFoundError:
            logger.debug(f"Toy not found for deletion: {toy_id_str}")
            return False

    async def close(self):
        """Close underlying Cosmos DB client if initialized.

        Safe to call multiple times; logs and suppresses any close errors.
        """
        if self._client:
            try:
                # Async CosmosClient implements close() to release network resources
                await self._client.close()
                logger.info("Cosmos client closed")
            except Exception as e:
                logger.warning(f"Failed to close Cosmos client: {e}")
