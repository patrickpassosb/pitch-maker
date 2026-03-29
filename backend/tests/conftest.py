from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from config import Settings
from main import create_app
from services.job_store import job_store


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    music_path = (
        Path(__file__).resolve().parents[2]
        / "assets"
        / "music"
        / "background.mp3"
    )
    return Settings(
        mock_external_services=True,
        jobs_dir=tmp_path / "jobs",
        background_music_path=music_path,
        allowed_origins=["http://localhost:5173"],
    )


@pytest.fixture
def client(test_settings: Settings) -> Generator[TestClient, None, None]:
    job_store.clear()
    app = create_app(test_settings)
    with TestClient(app) as test_client:
        yield test_client
    job_store.clear()
