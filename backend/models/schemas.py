from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class VisualMode(StrEnum):
    IMAGE = "image"
    VIDEO = "video"


class StepStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


class PipelineStep(StrEnum):
    GENERATING_SCRIPT = "generating_script"
    GENERATING_VOICE = "generating_voice"
    GENERATING_VISUALS = "generating_visuals"
    ASSEMBLING_VIDEO = "assembling_video"
    DONE = "done"


class GenerateRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=10, max_length=2_000)
    target_audience: str = Field(min_length=2, max_length=200)
    key_features: str = Field(min_length=3, max_length=2_000)
    duration_seconds: Literal[30, 60, 90]
    visual_mode: VisualMode = VisualMode.IMAGE

    @field_validator("project_name", "description", "target_audience", "key_features")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Field cannot be empty")
        return normalized


class GenerateResponse(BaseModel):
    job_id: str
    status: Literal["started"]


class Scene(BaseModel):
    scene_number: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=120)
    narration: str = Field(min_length=10, max_length=2_000)
    visual_prompt: str = Field(min_length=10, max_length=2_000)
    duration_seconds: int = Field(ge=1, le=90)


class PitchScript(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    total_duration_seconds: int = Field(ge=30, le=90)
    scenes: list[Scene] = Field(min_length=1, max_length=6)

    @model_validator(mode="after")
    def validate_script(self) -> PitchScript:
        total_duration = sum(scene.duration_seconds for scene in self.scenes)
        if total_duration != self.total_duration_seconds:
            raise ValueError("Scene durations must equal total_duration_seconds")

        expected_numbers = list(range(1, len(self.scenes) + 1))
        actual_numbers = [scene.scene_number for scene in self.scenes]
        if actual_numbers != expected_numbers:
            raise ValueError("Scene numbers must be sequential and start at 1")

        return self


class JobStatus(BaseModel):
    job_id: str
    status: Literal["processing", "completed", "error"]
    current_step: str
    steps: dict[str, StepStatus]
    video_url: str | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok"]
