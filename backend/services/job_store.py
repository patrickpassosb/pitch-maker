from __future__ import annotations

from threading import RLock

from models.schemas import JobStatus, PipelineStep, StepStatus


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobStatus] = {}
        self._lock = RLock()

    def create(self, job_id: str) -> JobStatus:
        job = JobStatus(
            job_id=job_id,
            status="processing",
            current_step=PipelineStep.GENERATING_SCRIPT.value,
            steps={
                PipelineStep.GENERATING_SCRIPT.value: StepStatus.PENDING,
                PipelineStep.GENERATING_VOICE.value: StepStatus.PENDING,
                PipelineStep.GENERATING_VISUALS.value: StepStatus.PENDING,
                PipelineStep.ASSEMBLING_VIDEO.value: StepStatus.PENDING,
            },
            video_url=None,
            error=None,
        )
        with self._lock:
            self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> JobStatus | None:
        with self._lock:
            return self._jobs.get(job_id)

    def update_step(
        self,
        job_id: str,
        step: PipelineStep,
        status: StepStatus,
        *,
        current_step: PipelineStep | None = None,
    ) -> JobStatus:
        with self._lock:
            job = self._jobs[job_id]
            job.steps[step.value] = status
            if current_step is not None:
                job.current_step = current_step.value
            return job

    def mark_completed(self, job_id: str, video_url: str) -> JobStatus:
        with self._lock:
            job = self._jobs[job_id]
            job.status = "completed"
            job.current_step = PipelineStep.DONE.value
            job.video_url = video_url
            return job

    def mark_error(self, job_id: str, message: str) -> JobStatus:
        with self._lock:
            job = self._jobs[job_id]
            job.status = "error"
            job.error = message
            for key, value in list(job.steps.items()):
                if value == StepStatus.IN_PROGRESS:
                    job.steps[key] = StepStatus.ERROR
            return job

    def clear(self) -> None:
        with self._lock:
            self._jobs.clear()


job_store = JobStore()
