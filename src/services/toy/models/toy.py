"""Data models for the toy service."""
from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer


class ToyBase(BaseModel):
    """Base toy model with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Display name of the toy")
    description: str | None = Field(None, max_length=500, description="Toy description or backstory")


class ToyCreate(ToyBase):
    """Model for creating a new toy."""

    id: UUID | None = Field(None, description="Optional explicit toy ID (for imports); auto-generated if omitted")


class ToyUpdate(BaseModel):
    """Model for updating a toy (partial update)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str | None) -> str | None:
        """Ensure name is not just whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v.strip() if v else None


class Toy(ToyBase):
    """Complete toy model with all fields."""

    id: UUID = Field(default_factory=uuid4, description="Unique toy identifier")
    avatar_blob_name: str | None = Field(None, description="Internal blob storage reference")
    has_avatar: bool = Field(False, description="Indicates if toy has an avatar image")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Registration timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Last modification timestamp")

    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        """Serialize UUID to string."""
        return str(value)

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value else None


class ToyDocument(Toy):
    """Toy model for Cosmos DB storage (includes partition key field)."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    # Cosmos DB fields
    toy_id: str = Field(alias="id", description="Partition key (same as id)")

    @field_serializer('toy_id')
    def serialize_toy_id(self, value: UUID | str) -> str:
        """Serialize toy_id field to string."""
        return str(value)

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, value):
        """Parse datetime strings from Cosmos DB, handling various formats."""
        if isinstance(value, str):
            # Handle strings with Z suffix and timezone offset (invalid format from old data)
            if value.endswith('+00:00Z'):
                value = value[:-1]  # Remove the 'Z' suffix, keep the timezone offset
            elif value.endswith('Z'):
                # Replace Z with +00:00 for proper timezone parsing
                value = value[:-1] + '+00:00'
            
            # Parse the string back to datetime
            return datetime.fromisoformat(value)
        return value

    @classmethod
    def from_toy(cls, toy: Toy) -> "ToyDocument":
        """Create a Cosmos DB document from a Toy model."""
        # Extract data without using model_dump to avoid serialization issues
        data = {
            "name": toy.name,
            "description": toy.description,
            "id": str(toy.id),  # Convert UUID to string
            "toy_id": str(toy.id),
            "avatar_blob_name": toy.avatar_blob_name,
            "has_avatar": toy.has_avatar,
            "created_at": toy.created_at,  # Keep as datetime object
            "updated_at": toy.updated_at,  # Keep as datetime object
        }
        return cls(**data)

    def to_toy(self) -> Toy:
        """Convert Cosmos DB document to Toy model."""
        data = self.model_dump(exclude={"toy_id"})
        return Toy(**data)
