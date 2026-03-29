from __future__ import annotations

import asyncio
import subprocess
from functools import lru_cache
from pathlib import Path

from config import Settings
from models.schemas import PitchScript


async def assemble_video(
    script: PitchScript,
    voice_path: Path,
    visual_paths: list[Path],
    job_dir: Path,
    settings: Settings,
) -> Path:
    output_path = job_dir / "output.mp4"
    command = build_ffmpeg_command(
        script=script,
        voice_path=voice_path,
        visual_paths=visual_paths,
        output_path=output_path,
        settings=settings,
    )

    result = await asyncio.to_thread(
        subprocess.run,
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr[-700:]}")
    return output_path


def build_ffmpeg_command(
    *,
    script: PitchScript,
    voice_path: Path,
    visual_paths: list[Path],
    output_path: Path,
    settings: Settings,
) -> list[str]:
    inputs: list[str] = [settings.ffmpeg_binary, "-y", "-threads", "1"]
    filter_parts: list[str] = []
    use_drawtext = False
    mock_scene_duration = 1 if settings.mock_external_services else None

    for index, (scene, visual_path) in enumerate(zip(script.scenes, visual_paths, strict=True)):
        scene_duration = mock_scene_duration or scene.duration_seconds
        if visual_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            inputs.extend(
                [
                    "-loop",
                    "1",
                    "-framerate",
                    "24",
                    "-t",
                    str(scene_duration),
                    "-i",
                    str(visual_path),
                ]
            )
            filter_parts.append(
                _image_filter(
                    index=index,
                    title=scene.title,
                    duration_seconds=scene_duration,
                    use_drawtext=use_drawtext,
                )
            )
        else:
            inputs.extend(["-i", str(visual_path)])
            filter_parts.append(
                _video_filter(
                    index=index,
                    title=scene.title,
                    duration_seconds=scene_duration,
                    use_drawtext=use_drawtext,
                )
            )

    narration_index = len(visual_paths)
    inputs.extend(["-i", str(voice_path)])

    total_duration = (
        len(visual_paths)
        if settings.mock_external_services
        else script.total_duration_seconds
    )
    include_music = False

    concat_inputs = "".join(f"[v{index}]" for index in range(len(visual_paths)))
    filter_parts.append(f"{concat_inputs}concat=n={len(visual_paths)}:v=1:a=0[outv]")
    filter_parts.append(f"[{narration_index}:a]atrim=duration={total_duration},asetpts=PTS-STARTPTS[voice]")

    filter_parts.append("[voice]anull[outa]")

    return [
        *inputs,
        "-filter_complex",
        ";".join(filter_parts),
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(output_path),
    ]


def _image_filter(
    *,
    index: int,
    title: str,
    duration_seconds: int,
    use_drawtext: bool,
) -> str:
    filter_chain = (
        f"[{index}:v]scale=960:540:force_original_aspect_ratio=increase,"
        "crop=960:540,"
    )
    if use_drawtext:
        escaped_title = _escape_text(title)
        filter_chain += (
            f"drawtext=text='{escaped_title}':fontcolor=white:fontsize=54:borderw=3:"
            "bordercolor=black@0.7:x=(w-text_w)/2:y=h-170,"
        )
    return f"{filter_chain}setsar=1[v{index}]"


def _video_filter(
    *,
    index: int,
    title: str,
    duration_seconds: int,
    use_drawtext: bool,
) -> str:
    filter_chain = (
        f"[{index}:v]trim=duration={duration_seconds},setpts=PTS-STARTPTS,"
        "fps=24,scale=960:540:force_original_aspect_ratio=increase,crop=960:540,"
    )
    if use_drawtext:
        escaped_title = _escape_text(title)
        filter_chain += (
            f"drawtext=text='{escaped_title}':fontcolor=white:fontsize=54:borderw=3:"
            "bordercolor=black@0.7:x=(w-text_w)/2:y=h-170,"
        )
    return f"{filter_chain}setsar=1[v{index}]"


def _escape_text(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", r"\'")
        .replace(",", "\\,")
        .replace("%", "\\%")
    )


@lru_cache
def ffmpeg_supports_drawtext(ffmpeg_binary: str) -> bool:
    result = subprocess.run(
        [ffmpeg_binary, "-hide_banner", "-filters"],
        capture_output=True,
        text=True,
        check=False,
    )
    return " drawtext " in result.stdout or " drawtext " in result.stderr
