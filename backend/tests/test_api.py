from __future__ import annotations

import time
from typing import Any, cast

from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_rejects_invalid_duration(client: TestClient) -> None:
    response = client.post(
        "/api/generate",
        json={
            "project_name": "Pitch Maker",
            "description": "Transforms project specs into cinematic pitch videos.",
            "target_audience": "Hackathon teams",
            "key_features": "Script generation\nVoiceover\nVisual creation",
            "duration_seconds": 45,
            "visual_mode": "image",
        },
    )

    assert response.status_code == 422


def test_full_generation_flow_with_mock_services(client: TestClient) -> None:
    response = client.post(
        "/api/generate",
        json={
            "project_name": "Pitch Maker",
            "description": "Transforms project specs into cinematic pitch videos in minutes.",
            "target_audience": "Hackathon teams and developers",
            "key_features": "Script generation\nVoiceover\nVisual creation\nMP4 export",
            "duration_seconds": 30,
            "visual_mode": "video",
        },
    )

    assert response.status_code == 200
    job_id = response.json()["job_id"]

    status_payload: dict[str, Any] | None = None
    for _ in range(60):
        status_response = client.get(f"/api/status/{job_id}")
        assert status_response.status_code == 200
        status_payload = status_response.json()
        if status_payload["status"] == "completed":
            break
        time.sleep(0.1)

    assert status_payload is not None
    assert status_payload["status"] == "completed"
    assert status_payload["current_step"] == "done"
    assert status_payload["video_url"] == f"/api/video/{job_id}/output.mp4"
    assert set(status_payload["steps"].values()) == {"completed"}

    video_url = cast(str, status_payload["video_url"])
    video_response = client.get(video_url)
    assert video_response.status_code == 200
    assert video_response.headers["content-type"] == "video/mp4"
    assert len(video_response.content) > 0


def test_missing_job_returns_not_found(client: TestClient) -> None:
    response = client.get("/api/status/unknown-job")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}
