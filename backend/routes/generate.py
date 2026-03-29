from __future__ import annotations

import asyncio
import logging
import uuid
from typing import cast

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse

from config import Settings
from models.schemas import (
    GenerateRequest,
    GenerateResponse,
    JobStatus,
    PipelineStep,
    StepStatus,
)
from services.job_store import job_store
from services.script_generator import generate_script
from services.video_assembler import assemble_video
from services.visual_generator import generate_visuals
from services.voice_generator import generate_voice

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=GenerateResponse)
async def generate_pitch(
    request_data: GenerateRequest,
    background_tasks: BackgroundTasks,
    request: Request,
) -> GenerateResponse:
    settings = _get_settings(request)
    job_id = str(uuid.uuid4())
    job_store.create(job_id)

    job_dir = settings.jobs_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    background_tasks.add_task(run_pipeline, job_id, request_data, settings)
    return GenerateResponse(job_id=job_id, status="started")


@router.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str) -> JobStatus:
    job = job_store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/video/{job_id}/{filename}")
async def get_video(job_id: str, filename: str, request: Request) -> FileResponse:
    settings = _get_settings(request)
    job_dir = (settings.jobs_dir / job_id).resolve()
    file_path = (job_dir / filename).resolve()

    if not file_path.exists() or job_dir not in file_path.parents:
        raise HTTPException(status_code=404, detail="Video not found")

    media_type = "video/mp4" if file_path.suffix.lower() == ".mp4" else "application/octet-stream"
    return FileResponse(path=file_path, filename=file_path.name, media_type=media_type)


async def run_pipeline(job_id: str, request_data: GenerateRequest, settings: Settings) -> None:
    job_dir = settings.jobs_dir / job_id

    try:
        logger.info("Starting pipeline for job %s", job_id)

        job_store.update_step(
            job_id,
            PipelineStep.GENERATING_SCRIPT,
            StepStatus.IN_PROGRESS,
            current_step=PipelineStep.GENERATING_SCRIPT,
        )
        script = await generate_script(request_data, settings)
        (job_dir / "script.json").write_text(script.model_dump_json(indent=2), encoding="utf-8")
        job_store.update_step(job_id, PipelineStep.GENERATING_SCRIPT, StepStatus.COMPLETED)

        job_store.update_step(
            job_id,
            PipelineStep.GENERATING_VOICE,
            StepStatus.IN_PROGRESS,
            current_step=PipelineStep.GENERATING_VOICE,
        )
        job_store.update_step(job_id, PipelineStep.GENERATING_VISUALS, StepStatus.IN_PROGRESS)

        voice_path, visual_paths = await asyncio.gather(
            generate_voice(script, job_dir, settings),
            generate_visuals(script, job_dir, request_data.visual_mode, settings),
        )

        job_store.update_step(job_id, PipelineStep.GENERATING_VOICE, StepStatus.COMPLETED)
        job_store.update_step(job_id, PipelineStep.GENERATING_VISUALS, StepStatus.COMPLETED)

        job_store.update_step(
            job_id,
            PipelineStep.ASSEMBLING_VIDEO,
            StepStatus.IN_PROGRESS,
            current_step=PipelineStep.ASSEMBLING_VIDEO,
        )
        output_path = await assemble_video(script, voice_path, visual_paths, job_dir, settings)
        job_store.update_step(job_id, PipelineStep.ASSEMBLING_VIDEO, StepStatus.COMPLETED)
        job_store.mark_completed(job_id, f"{settings.api_prefix}/video/{job_id}/{output_path.name}")
        logger.info("Completed pipeline for job %s", job_id)
    except Exception as exc:
        logger.exception("Pipeline failed for job %s", job_id)
        job_store.mark_error(job_id, str(exc))


def _get_settings(request: Request) -> Settings:
    settings = getattr(request.app.state, "settings", None)
    if settings is None:
        raise RuntimeError("Application settings are not configured")
    return cast(Settings, settings)
