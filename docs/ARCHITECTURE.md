# Pitch Maker — Architecture Document

## System Architecture Overview

```
┌──────────────────────────────────────────────────┐
│                  FRONTEND                         │
│           React + TypeScript + Vite               │
│                                                   │
│  InputPage ──→ GeneratingPage ──→ ResultPage      │
│  (form)        (polling)          (video player)  │
└───────────────────┬──────────────────────────────┘
                    │ HTTP (fetch)
                    │ POST /api/generate
                    │ GET  /api/status/{id}
                    │ GET  /api/video/{id}/{file}
┌───────────────────┴──────────────────────────────┐
│                  BACKEND                          │
│            Python + FastAPI + asyncio             │
│                                                   │
│  ┌─────────────┐                                  │
│  │ POST /api/  │──→ Background Task               │
│  │ generate    │         │                        │
│  └─────────────┘         ▼                        │
│                 ┌─────────────────┐               │
│                 │ STEP 1: Mistral │               │
│                 │ Script Gen      │               │
│                 └────────┬────────┘               │
│                          ▼                        │
│              ┌───────────┴───────────┐            │
│              ▼                       ▼            │
│    ┌──────────────────┐  ┌────────────────────┐   │
│    │ STEP 2a:         │  │ STEP 2b:           │   │
│    │ ElevenLabs TTS   │  │ fal.ai Visuals     │   │
│    │ (voice)          │  │ (images or video)  │   │
│    └────────┬─────────┘  └──────────┬─────────┘   │
│             └───────────┬───────────┘             │
│                         ▼                         │
│              ┌─────────────────────┐              │
│              │ STEP 3: FFmpeg      │              │
│              │ Video Assembly      │              │
│              └────────┬────────────┘              │
│                       ▼                           │
│                  output.mp4                       │
└──────────────────────────────────────────────────┘
```

---

## Backend Service Details

### config.py — Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mistral_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str = "JBFqnCBsd6RMkjVDRZzb"
    fal_key: str
    jobs_dir: str = "jobs"

    class Config:
        env_file = ".env"

settings = Settings()
```

### models/schemas.py — Pydantic Models

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class VisualMode(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class GenerateRequest(BaseModel):
    project_name: str
    description: str
    target_audience: str
    key_features: str
    duration_seconds: int  # 30, 60, or 90
    visual_mode: VisualMode = VisualMode.IMAGE

class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

class JobStatus(BaseModel):
    job_id: str
    status: str  # "processing", "completed", "error"
    current_step: str
    steps: dict[str, str]
    video_url: Optional[str] = None
    error: Optional[str] = None

class Scene(BaseModel):
    scene_number: int
    title: str
    narration: str
    visual_prompt: str
    duration_seconds: int

class PitchScript(BaseModel):
    title: str
    total_duration_seconds: int
    scenes: list[Scene]
```

### main.py — FastAPI App

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.generate import router
import os

app = FastAPI(title="Pitch Maker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure jobs directory exists
os.makedirs("jobs", exist_ok=True)

app.include_router(router, prefix="/api")
```

### routes/generate.py — API Routes

```python
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from models.schemas import GenerateRequest, JobStatus
import uuid
import asyncio
import os

router = APIRouter()

# In-memory job store
jobs: dict[str, dict] = {}

@router.post("/generate")
async def generate_pitch(request: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "processing",
        "current_step": "generating_script",
        "steps": {
            "generating_script": "pending",
            "generating_voice": "pending",
            "generating_visuals": "pending",
            "assembling_video": "pending",
        },
        "video_url": None,
        "error": None,
    }
    
    # Create job directory
    job_dir = f"jobs/{job_id}"
    os.makedirs(job_dir, exist_ok=True)
    
    # Run pipeline in background
    background_tasks.add_task(run_pipeline, job_id, request)
    
    return {"job_id": job_id, "status": "started"}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@router.get("/video/{job_id}/{filename}")
async def get_video(job_id: str, filename: str):
    filepath = f"jobs/{job_id}/{filename}"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(filepath, media_type="video/mp4")

async def run_pipeline(job_id: str, request: GenerateRequest):
    """Main pipeline: script → (voice + visuals) parallel → assembly"""
    from services.script_generator import generate_script
    from services.voice_generator import generate_voice
    from services.visual_generator import generate_visuals
    from services.video_assembler import assemble_video
    
    job = jobs[job_id]
    job_dir = f"jobs/{job_id}"
    
    try:
        # Step 1: Generate script
        job["steps"]["generating_script"] = "in_progress"
        script = await generate_script(request)
        # Save script for reference
        import json
        with open(f"{job_dir}/script.json", "w") as f:
            json.dump(script.dict(), f, indent=2)
        job["steps"]["generating_script"] = "completed"
        
        # Step 2a + 2b: Voice and visuals in parallel
        job["current_step"] = "generating_voice"
        job["steps"]["generating_voice"] = "in_progress"
        job["steps"]["generating_visuals"] = "in_progress"
        
        voice_path, visual_paths = await asyncio.gather(
            generate_voice(script, job_dir),
            generate_visuals(script, job_dir, request.visual_mode),
        )
        
        job["steps"]["generating_voice"] = "completed"
        job["steps"]["generating_visuals"] = "completed"
        
        # Step 3: Assemble video
        job["current_step"] = "assembling_video"
        job["steps"]["assembling_video"] = "in_progress"
        
        output_path = await assemble_video(
            script=script,
            voice_path=voice_path,
            visual_paths=visual_paths,
            job_dir=job_dir,
            visual_mode=request.visual_mode,
        )
        
        job["steps"]["assembling_video"] = "completed"
        job["status"] = "completed"
        job["current_step"] = "done"
        job["video_url"] = f"/api/video/{job_id}/output.mp4"
        
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        # Mark current step as error
        for step_name, step_status in job["steps"].items():
            if step_status == "in_progress":
                job["steps"][step_name] = "error"
```

---

## Service Implementation Patterns

### script_generator.py

```python
from mistralai import Mistral
from models.schemas import GenerateRequest, PitchScript
from config import settings
import json

async def generate_script(request: GenerateRequest) -> PitchScript:
    client = Mistral(api_key=settings.mistral_api_key)
    
    # See PROMPTS.md for the full system prompt
    system_prompt = "..."  # Load from PROMPTS.md
    
    user_prompt = f"""Generate a cinematic pitch for this project:

Project Name: {request.project_name}
Description: {request.description}
Target Audience: {request.target_audience}
Key Features: {request.key_features}
Total Duration: {request.duration_seconds} seconds
Number of scenes: {request.duration_seconds // 15 + 1}"""

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    
    result = json.loads(response.choices[0].message.content)
    return PitchScript(**result)
```

### voice_generator.py

```python
from elevenlabs.client import ElevenLabs
from models.schemas import PitchScript
from config import settings

async def generate_voice(script: PitchScript, job_dir: str) -> str:
    client = ElevenLabs(api_key=settings.elevenlabs_api_key)
    
    # Concatenate narrations with pauses between scenes
    full_narration = ' <break time="0.8s"/> '.join(
        scene.narration for scene in script.scenes
    )
    
    audio = client.text_to_speech.convert(
        text=full_narration,
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
    
    output_path = f"{job_dir}/narration.mp3"
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    
    return output_path
```

### visual_generator.py

```python
import fal_client
import asyncio
import httpx
from models.schemas import PitchScript
from config import settings

async def generate_visuals(
    script: PitchScript,
    job_dir: str,
    visual_mode: str,
) -> list[str]:
    """Generate visuals for each scene. Returns list of file paths."""
    
    if visual_mode == "image":
        return await generate_images(script, job_dir)
    else:
        return await generate_video_clips(script, job_dir)

async def generate_images(script: PitchScript, job_dir: str) -> list[str]:
    """Generate all scene images in parallel."""
    
    async def generate_one_image(scene) -> str:
        prompt = f"{scene.visual_prompt}, cinematic photography, 16:9 aspect ratio, high detail, dramatic lighting, National Geographic documentary style"
        
        result = await fal_client.subscribe_async(
            "fal-ai/flux-pro/v1.1-ultra",
            arguments={
                "prompt": prompt,
                "image_size": {"width": 1920, "height": 1080},
            },
        )
        
        # Download the generated image
        image_url = result["images"][0]["url"]
        output_path = f"{job_dir}/scene_{scene.scene_number}.png"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            with open(output_path, "wb") as f:
                f.write(response.content)
        
        return output_path
    
    # Generate all images in parallel
    paths = await asyncio.gather(
        *[generate_one_image(scene) for scene in script.scenes]
    )
    return list(paths)

async def generate_video_clips(script: PitchScript, job_dir: str) -> list[str]:
    """Generate video clips sequentially (Kling concurrency limits)."""
    paths = []
    
    for scene in script.scenes:
        try:
            result = await fal_client.subscribe_async(
                "fal-ai/kling-video/v2.5/standard/text-to-video",
                arguments={
                    "prompt": scene.visual_prompt,
                    "duration": "5",
                    "aspect_ratio": "16:9",
                },
            )
            
            video_url = result["video"]["url"]
            output_path = f"{job_dir}/scene_{scene.scene_number}.mp4"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(video_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)
            
            paths.append(output_path)
            
        except Exception:
            # Fallback: generate image instead
            fallback_path = await generate_images_single(scene, job_dir)
            paths.append(fallback_path)
    
    return paths
```

### video_assembler.py

```python
import subprocess
import os
from models.schemas import PitchScript

async def assemble_video(
    script: PitchScript,
    voice_path: str,
    visual_paths: list[str],
    job_dir: str,
    visual_mode: str,
) -> str:
    """Assemble final video using FFmpeg."""
    
    output_path = f"{job_dir}/output.mp4"
    music_path = "assets/music/background.mp3"
    
    # Build FFmpeg command dynamically based on scenes
    inputs = []
    filter_parts = []
    
    for i, (scene, visual_path) in enumerate(zip(script.scenes, visual_paths)):
        is_image = visual_path.endswith(".png") or visual_path.endswith(".jpg")
        
        if is_image:
            # Image input with loop
            inputs.extend(["-loop", "1", "-t", str(scene.duration_seconds), "-i", visual_path])
        else:
            # Video input
            inputs.extend(["-i", visual_path])
        
        # Ken Burns zoom effect + title overlay + fade
        filter_parts.append(
            f"[{i}:v]"
            f"scale=2048:1152,zoompan=z='min(zoom+0.0003,1.1)':d={30*scene.duration_seconds}:s=1920x1080:fps=30,"
            f"drawtext=text='{scene.title}':fontsize=52:fontcolor=white:"
            f"borderw=3:bordercolor=black@0.7:"
            f"x=(w-text_w)/2:y=(h-text_h)/2+300:"
            f"enable='between(t,0.5,{scene.duration_seconds-0.5})':"
            f"alpha='if(lt(t,1.5),t-0.5,if(gt(t,{scene.duration_seconds-1.5}),{scene.duration_seconds-0.5}-t,1))',"
            f"fade=t=in:st=0:d=0.5,fade=t=out:st={scene.duration_seconds-0.5}:d=0.5"
            f"[v{i}]"
        )
    
    # Concat all video segments
    concat_inputs = "".join(f"[v{i}]" for i in range(len(script.scenes)))
    filter_parts.append(f"{concat_inputs}concat=n={len(script.scenes)}:v=1:a=0[outv]")
    
    # Audio: narration input index
    narration_idx = len(script.scenes)
    music_idx = narration_idx + 1
    
    inputs.extend(["-i", voice_path])
    inputs.extend(["-i", music_path])
    
    # Audio mixing
    total_duration = script.total_duration_seconds
    filter_parts.append(f"[{narration_idx}:a]volume=1.0[voice]")
    filter_parts.append(
        f"[{music_idx}:a]volume=0.15,"
        f"afade=t=in:st=0:d=2,"
        f"afade=t=out:st={total_duration-3}:d=3"
        f"[music]"
    )
    filter_parts.append("[voice][music]amix=inputs=2:duration=first[outa]")
    
    filter_complex = ";\n".join(filter_parts)
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        output_path,
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg error: {result.stderr[-500:]}")
    
    return output_path
```

---

## Frontend API Client Pattern

### api/client.ts

```typescript
const API_BASE = "/api";

export interface GenerateRequest {
  project_name: string;
  description: string;
  target_audience: string;
  key_features: string;
  duration_seconds: 30 | 60 | 90;
  visual_mode: "image" | "video";
}

export interface JobStatus {
  job_id: string;
  status: "processing" | "completed" | "error";
  current_step: string;
  steps: Record<string, string>;
  video_url: string | null;
  error: string | null;
}

export async function generatePitch(data: GenerateRequest): Promise<{ job_id: string }> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to start generation");
  return res.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatus> {
  const res = await fetch(`${API_BASE}/status/${jobId}`);
  if (!res.ok) throw new Error("Failed to get status");
  return res.json();
}
```

### Polling pattern in GeneratingPage.tsx

```typescript
useEffect(() => {
  const interval = setInterval(async () => {
    const status = await getJobStatus(jobId);
    setJobStatus(status);
    
    if (status.status === "completed") {
      clearInterval(interval);
      navigate(`/result/${jobId}`);
    }
    
    if (status.status === "error") {
      clearInterval(interval);
      setError(status.error);
    }
  }, 2000);
  
  return () => clearInterval(interval);
}, [jobId]);
```

---

## Key Technical Decisions

1. **In-memory job store** — No database. Jobs dict lives in FastAPI process. Fine for hackathon demo, not for production.

2. **Background tasks** — `BackgroundTasks` from FastAPI runs the pipeline after returning the job ID immediately. Frontend doesn't wait.

3. **Async parallel** — Voice and visuals generate simultaneously via `asyncio.gather()`. Script must finish first since both depend on it.

4. **FFmpeg via subprocess** — More reliable than MoviePy for a hackathon. Fewer dependencies, more control, better error messages.

5. **Vite proxy** — Frontend dev server proxies `/api/*` to backend at port 8000. No CORS issues in development.

6. **Fallback strategy** — If Kling video fails for any scene, fall back to generating an image. The assembler handles mixed inputs.
