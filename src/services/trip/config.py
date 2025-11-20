"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Azure Authentication
    azure_tenant_id: str
    app_id_uri: str
    # Managed Identity Client ID (optional - for explicit identity selection)
    azure_client_id: str | None = None

    # Cosmos DB
    cosmos_endpoint: str
    cosmos_database_name: str = "toytripdb"
    cosmos_container_name: str = "trips"
    cosmos_key: str | None = None
    cosmos_disable_ssl_verify: bool = False

    # Blob Storage
    storage_account_url: str
    storage_account_key: str | None = None
    blob_container_gallery: str = "gallery"

    # Inter-service Communication
    toy_service_url: str = "http://localhost:8001"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8002
    log_level: str = "INFO"

    # Testing (optional)
    test_client_secret: str | None = None


# Global settings instance
settings = Settings()
