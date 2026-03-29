from __future__ import annotations

import asyncio
import json
from typing import Any, cast

from mistralai import Mistral

from config import Settings
from models.schemas import GenerateRequest, PitchScript, Scene
from services.prompt_loader import (
    SCENE_COUNT_BY_DURATION,
    build_mistral_user_prompt,
    load_mistral_system_prompt,
)


async def generate_script(request: GenerateRequest, settings: Settings) -> PitchScript:
    if settings.mock_external_services:
        return build_mock_script(request)

    if not settings.mistral_api_key:
        raise RuntimeError("Mistral API key is missing")

    client = Mistral(api_key=settings.mistral_api_key)
    system_prompt = load_mistral_system_prompt()
    user_prompt = build_mistral_user_prompt(request)

    messages = cast(
        Any,
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    response = await asyncio.to_thread(
        client.chat.complete,
        model="mistral-large-latest",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    content = _extract_response_content(response)
    payload = json.loads(content)
    return PitchScript.model_validate(payload)


def build_mock_script(request: GenerateRequest) -> PitchScript:
    scene_count = SCENE_COUNT_BY_DURATION[request.duration_seconds]
    base_duration = request.duration_seconds // scene_count
    durations = [base_duration] * scene_count
    durations[-1] += request.duration_seconds - sum(durations)

    feature_lines = [line.strip() for line in request.key_features.splitlines() if line.strip()]
    if not feature_lines:
        feature_lines = ["Intelligent automation", "Cinematic storytelling", "Instant delivery"]

    scene_templates: list[dict[str, str]] = [
        {
            "title": "The Opportunity",
            "narration": (
                f"{request.project_name} begins with a clear mission. {request.description} "
                f"It is designed for {request.target_audience}, turning an ambitious idea into "
                "a vivid story."
            ),
            "visual_prompt": (
                f"A cinematic opening shot representing {request.project_name}, "
                "dramatic lighting, editorial composition, premium product "
                f"storytelling, audience of {request.target_audience}"
            ),
        },
        {
            "title": "The Problem",
            "narration": (
                "Too often, teams struggle to explain why their work matters. "
                f"{request.project_name} frames the challenge with clarity and urgency, "
                "making the value instantly understandable."
            ),
            "visual_prompt": (
                "A dramatic scene showing the tension of innovation meeting "
                "communication barriers, "
                "dark environment, focused subject, documentary realism"
            ),
        },
        {
            "title": "The Solution",
            "narration": (
                f"Here is the answer: {request.project_name}. It combines "
                f"{feature_lines[0].lower()} "
                "with a polished workflow that feels effortless from start to finish."
            ),
            "visual_prompt": (
                f"A premium interface reveal for {request.project_name}, glowing screens, "
                "gold accents, cinematic product photography"
            ),
        },
        {
            "title": "The Features",
            "narration": (
                "Its standout features do more than save time. They shape a "
                "complete experience through "
                f"{', '.join(feature_lines[:3]).lower()}."
            ),
            "visual_prompt": (
                "A stylized montage of product features represented as cinematic panels, "
                "high contrast, dramatic depth, elegant motion cues"
            ),
        },
        {
            "title": "The Impact",
            "narration": (
                f"For {request.target_audience}, the result is momentum. "
                f"{request.project_name} helps teams "
                "move from concept to confidence with a story strong enough to be remembered."
            ),
            "visual_prompt": (
                "An inspiring closing scene with an engaged audience and a large "
                "screen presentation, "
                "warm glow, triumphant documentary framing"
            ),
        },
        {
            "title": "The Future",
            "narration": (
                f"This is only the beginning. {request.project_name} points toward "
                "a future where powerful "
                "ideas are not just built well, but presented with cinematic conviction."
            ),
            "visual_prompt": (
                "A visionary futuristic tableau, sweeping light beams, cinematic horizon, "
                "hopeful and ambitious mood"
            ),
        },
    ]

    scenes = [
        Scene(
            scene_number=index + 1,
            title=scene_templates[index]["title"],
            narration=scene_templates[index]["narration"],
            visual_prompt=scene_templates[index]["visual_prompt"],
            duration_seconds=durations[index],
        )
        for index in range(scene_count)
    ]

    return PitchScript(
        title=request.project_name,
        total_duration_seconds=request.duration_seconds,
        scenes=scenes,
    )


def _extract_response_content(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [item.get("text", "") for item in content if isinstance(item, dict)]
        return "".join(parts)
    raise RuntimeError("Unexpected Mistral response format")
