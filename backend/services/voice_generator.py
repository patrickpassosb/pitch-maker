from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

from elevenlabs.client import ElevenLabs

from config import Settings
from models.schemas import PitchScript


async def generate_voice(script: PitchScript, job_dir: Path, settings: Settings) -> Path:
    output_path = job_dir / "narration.mp3"

    if settings.mock_external_services:
        await _generate_silent_audio(output_path, script.total_duration_seconds, settings)
        return output_path

    if not settings.elevenlabs_api_key:
        raise RuntimeError("ElevenLabs API key is missing")

    client = ElevenLabs(api_key=settings.elevenlabs_api_key)
    narration = " <break time=\"0.8s\"/> ".join(scene.narration for scene in script.scenes)

    audio_stream = await asyncio.to_thread(
        client.text_to_speech.convert,
        text=narration,
        voice_id=settings.elevenlabs_voice_id,
        model_id="eleven_v3",
        output_format="mp3_44100_128",
        voice_settings={
            "stability": 0.4,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True,
        },
    )

    with output_path.open("wb") as file_handle:
        for chunk in audio_stream:
            file_handle.write(chunk)

    return output_path


async def _generate_silent_audio(
    output_path: Path,
    duration_seconds: int,
    settings: Settings,
) -> None:
    command = [
        settings.ffmpeg_binary,
        "-y",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=44100:cl=stereo",
        "-t",
        str(duration_seconds),
        "-q:a",
        "9",
        "-acodec",
        "libmp3lame",
        str(output_path),
    ]
    result = await asyncio.to_thread(
        subprocess.run,
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Unable to synthesize placeholder narration: {result.stderr[-500:]}"
        )
