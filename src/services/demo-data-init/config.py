"""Settings module for the demo data init service."""
from __future__ import annotations

from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_assets_path() -> Path:
    repo_data = Path(__file__).resolve().parents[3] / "tools" / "data"
    return repo_data if repo_data.exists() else Path(__file__).resolve().parent / "data"


class Settings(BaseSettings):
    """Central application configuration loaded from environment."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8010, alias="API_PORT")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    toy_service_url: str = Field(..., alias="TOY_SERVICE_URL")
    trip_service_url: str = Field(..., alias="TRIP_SERVICE_URL")

    assets_path: Path = Field(default_factory=_default_assets_path, alias="DEMO_DATA_ASSETS_PATH")

    http_timeout_seconds: int = Field(20, alias="DEMO_DATA_HTTP_TIMEOUT")
    max_retry_attempts: int = Field(3, alias="DEMO_DATA_HTTP_RETRIES")

    @field_validator('assets_path', mode='before')
    @classmethod
    def resolve_assets_path(cls, v):
        """Convert relative paths to absolute paths relative to this config file."""
        if isinstance(v, str):
            path = Path(v)
            if not path.is_absolute():
                # Resolve relative to the config file's directory
                config_dir = Path(__file__).resolve().parent
                path = (config_dir / path).resolve()
            return path
        return v


settings = Settings()
