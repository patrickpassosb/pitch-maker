from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Pitch Maker API"
    app_env: str = "development"
    api_prefix: str = "/api"
    log_level: str = "INFO"

    mistral_api_key: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "JBFqnCBsd6RMkjVDRZzb"
    fal_key: str = ""

    jobs_dir: Path = BASE_DIR / "jobs"
    docs_dir: Path = PROJECT_DIR / "docs"
    background_music_path: Path = PROJECT_DIR / "assets" / "music" / "background.mp3"
    ffmpeg_binary: str = "ffmpeg"

    allowed_origins: Annotated[
        list[str],
        NoDecode,
    ] = Field(default_factory=lambda: ["http://localhost:5173"])
    mock_external_services: bool = False

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
