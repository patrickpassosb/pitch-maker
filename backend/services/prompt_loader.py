from __future__ import annotations

import re

from config import get_settings
from models.schemas import GenerateRequest

SCENE_COUNT_BY_DURATION = {
    30: 3,
    60: 5,
    90: 6,
}


def load_mistral_system_prompt() -> str:
    prompts_path = get_settings().docs_dir / "PROMPTS.md"
    content = prompts_path.read_text(encoding="utf-8")
    match = re.search(
        r"## Mistral System Prompt \(Script Generation\)\s+.*?```(.*?)```",
        content,
        flags=re.DOTALL,
    )
    if match is None:
        raise RuntimeError("Unable to load the Mistral system prompt from PROMPTS.md")
    return match.group(1).strip()


def build_mistral_user_prompt(request: GenerateRequest) -> str:
    num_scenes = SCENE_COUNT_BY_DURATION[request.duration_seconds]
    return (
        "Generate a cinematic pitch for this project:\n\n"
        f"Project Name: {request.project_name}\n"
        f"Description: {request.description}\n"
        f"Target Audience: {request.target_audience}\n"
        "Key Features:\n"
        f"{request.key_features}\n\n"
        f"Total Duration: {request.duration_seconds} seconds\n"
        f"Number of scenes: {num_scenes}\n\n"
        f"Create exactly {num_scenes} scenes. "
        f"The sum of all scene durations must equal exactly {request.duration_seconds} seconds."
    )
