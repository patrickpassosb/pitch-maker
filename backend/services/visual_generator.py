from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, cast

import fal_client
import httpx
from PIL import Image, ImageDraw, ImageFont

from config import Settings
from models.schemas import PitchScript, Scene, VisualMode

VISUAL_SUFFIX = (
    ", cinematic photography, 16:9 aspect ratio, high detail, dramatic lighting, "
    "National Geographic documentary style, professional color grading, shallow depth of field"
)


async def generate_visuals(
    script: PitchScript,
    job_dir: Path,
    visual_mode: VisualMode,
    settings: Settings,
) -> list[Path]:
    if settings.mock_external_services:
        return [await generate_placeholder_image(scene, job_dir) for scene in script.scenes]

    if not settings.fal_key:
        raise RuntimeError("fal.ai API key is missing")
    os.environ["FAL_KEY"] = settings.fal_key

    if visual_mode == VisualMode.IMAGE:
        tasks = [generate_image(scene, job_dir, settings) for scene in script.scenes]
        return list(await asyncio.gather(*tasks))

    results: list[Path] = []
    for scene in script.scenes:
        try:
            results.append(await generate_video_clip(scene, job_dir))
        except Exception:
            results.append(await generate_placeholder_image(scene, job_dir))
    return results


async def generate_image(scene: Scene, job_dir: Path, settings: Settings) -> Path:
    prompt = f"{scene.visual_prompt}{VISUAL_SUFFIX}"
    try:
        result = await fal_client.subscribe_async(
            "fal-ai/flux-pro/v1.1-ultra",
            arguments={
                "prompt": prompt,
                "image_size": {
                    "width": 1920,
                    "height": 1080,
                },
            },
        )
        image_url = _extract_image_url(result)
        output_path = job_dir / f"scene_{scene.scene_number}.png"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(image_url)
            response.raise_for_status()
            output_path.write_bytes(response.content)
        return output_path
    except Exception:
        return await generate_placeholder_image(scene, job_dir)


async def generate_video_clip(scene: Scene, job_dir: Path) -> Path:
    result = await fal_client.subscribe_async(
        "fal-ai/kling-video/v2.5/standard/text-to-video",
        arguments={
            "prompt": f"{scene.visual_prompt}{VISUAL_SUFFIX}",
            "duration": "5",
            "aspect_ratio": "16:9",
        },
    )
    video_url = _extract_video_url(result)
    output_path = job_dir / f"scene_{scene.scene_number}.mp4"
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(video_url)
        response.raise_for_status()
        output_path.write_bytes(response.content)
    return output_path


async def generate_placeholder_image(scene: Scene, job_dir: Path) -> Path:
    output_path = job_dir / f"scene_{scene.scene_number}.png"
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), "#0e0e0e")
    draw = ImageDraw.Draw(image)

    for row in range(height):
        blend = row / height
        red = int(14 + (34 - 14) * blend)
        green = int(14 + (18 - 14) * blend)
        blue = int(14 + (18 - 14) * blend)
        draw.line([(0, row), (width, row)], fill=(red, green, blue))

    draw.ellipse((100, 120, 800, 820), fill=(242, 192, 98, 18))
    draw.ellipse((1220, 200, 1820, 800), fill=(212, 165, 74, 12))

    title_font = _load_font(96)
    body_font = _load_font(38)

    title_box = draw.textbbox((0, 0), scene.title.upper(), font=title_font)
    title_width = title_box[2] - title_box[0]
    draw.text(
        ((width - title_width) / 2, 360),
        scene.title.upper(),
        fill="#f2c062",
        font=title_font,
    )

    excerpt = scene.narration[:220].rsplit(" ", 1)[0] + "..."
    body_box = draw.multiline_textbbox((0, 0), excerpt, font=body_font, spacing=10)
    body_width = body_box[2] - body_box[0]
    draw.multiline_text(
        ((width - body_width) / 2, 500),
        excerpt,
        fill="#e5e2e1",
        font=body_font,
        align="center",
        spacing=10,
    )

    image.save(output_path)
    return output_path


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for font_name in ("DejaVuSerif.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(font_name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _extract_image_url(result: Any) -> str:
    images = result.get("images", [])
    if not images:
        raise RuntimeError("fal.ai did not return any images")
    return cast(str, images[0]["url"])


def _extract_video_url(result: Any) -> str:
    video = result.get("video")
    if not video or "url" not in video:
        raise RuntimeError("fal.ai did not return a video URL")
    return str(video["url"])
