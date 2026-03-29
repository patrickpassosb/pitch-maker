from __future__ import annotations

from models.schemas import GenerateRequest, VisualMode
from services.script_generator import build_mock_script


def test_build_mock_script_matches_duration_rules() -> None:
    request = GenerateRequest(
        project_name="Pitch Maker",
        description="Creates cinematic videos from project descriptions.",
        target_audience="Hackathon teams",
        key_features="Script generation\nVoiceover\nVisuals\nExports",
        duration_seconds=90,
        visual_mode=VisualMode.IMAGE,
    )

    script = build_mock_script(request)

    assert script.total_duration_seconds == 90
    assert len(script.scenes) == 6
    assert sum(scene.duration_seconds for scene in script.scenes) == 90
    assert [scene.scene_number for scene in script.scenes] == [1, 2, 3, 4, 5, 6]
