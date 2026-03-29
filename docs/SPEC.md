# Pitch Maker — Complete Project Specification

## What Is This Document?

This is the complete specification for **Pitch Maker**, an AI-powered tool that generates cinematic pitch videos for hackathon projects. Give this entire document to TRAE SOLO and say: **"Build this project following this specification exactly."**

---

## Project Overview

**Name:** Pitch Maker
**Tagline:** "Turn your project specs into a cinematic pitch video in minutes."
**What it does:** The user fills in a form with their project details (name, description, audience, features). The app generates a cinematic, National Geographic-style pitch video with AI-generated script, professional voiceover, AI-generated visuals, and background music — all assembled into a downloadable MP4.

**Core flow:**
1. User fills a form with project details
2. Mistral AI writes a cinematic pitch script (structured JSON)
3. ElevenLabs generates cinematic voiceover narration
4. fal.ai generates AI images (Flux Pro) or AI video clips (Kling)
5. FFmpeg assembles everything into a final MP4 with text overlays, transitions, and background music
6. User watches and downloads the video

---

## Tech Stack

### Frontend
- **React 18+** with **TypeScript**
- **Vite** as build tool and dev server (port 5173)
- **Tailwind CSS** for styling
- **React Router** for page navigation
- Dark cinematic UI theme

### Backend
- **Python 3.11+** with **FastAPI**
- **Uvicorn** ASGI server (port 8000)
- **asyncio** for parallel API calls
- **httpx** for async HTTP requests to external APIs

### External APIs
- **Mistral AI** — `mistral-large-latest` — Script generation (JSON output)
- **ElevenLabs** — `eleven_v3` model — Cinematic voiceover
- **fal.ai** — `fal-ai/flux-pro/v1.1-ultra` for images, `fal-ai/kling-video/v2.5/standard/text-to-video` for video clips

### Video Assembly
- **FFmpeg** — Called via Python `subprocess` — Combines images/clips + audio + text overlays + music into MP4

---

## Project File Structure

```
pitch-maker/
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── InputPage.tsx
│   │   │   ├── GeneratingPage.tsx
│   │   │   └── ResultPage.tsx
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── StepProgress.tsx
│   │   │   └── VideoPlayer.tsx
│   │   ├── api/
│   │   │   └── client.ts
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   └── generate.py
│   ├── services/
│   │   ├── script_generator.py
│   │   ├── voice_generator.py
│   │   ├── visual_generator.py
│   │   └── video_assembler.py
│   ├── models/
│   │   └── schemas.py
│   ├── jobs/
│   └── pyproject.toml
│
├── assets/
│   └── music/
│       └── background.mp3
│
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

## UI Specification — 3 Pages

The UI uses a **dark cinematic theme**: deep black backgrounds (#0a0a0a, #141414), subtle gradient accents, gold/amber highlights (#d4a54a, #f5c842), white text, cinematic serif font for headings (Playfair Display from Google Fonts), clean sans-serif for body (Inter).

### Page 1: Input Form (route: `/`)

- Full-screen dark background with subtle radial gradient
- Centered card (max-width 640px) with glass effect (bg-white/5 backdrop-blur)
- Title: "PITCH MAKER" in gold serif font with subtle glow
- Subtitle: "Turn your project into a cinematic pitch" in gray

**Form fields:**
1. **Project Name** — text input, placeholder: "e.g., Pitch Maker"
2. **What does it do?** — textarea (3 rows), placeholder: "Describe your project in 2-3 sentences..."
3. **Who is it for?** — text input, placeholder: "e.g., Hackathon participants, developers"
4. **Key Features** — textarea (4 rows), placeholder: "List 3-5 key features, one per line..."
5. **Pitch Duration** — 3 toggle buttons: `30s` | `60s` | `90s` (default: 60s)
6. **Visual Style** — toggle: `AI Images` (default, label: "Fast & reliable") | `AI Video Clips` (label: "Cinematic, takes 2-5 min longer")

**Submit button:** Large gold gradient button: "Generate Cinematic Pitch →"
**Styling:** All inputs dark bg (bg-white/10), white text, border-white/20, rounded-lg. Focus: gold border.

### Page 2: Generating (route: `/generating/:jobId`)

- Full-screen dark background
- Centered content (max-width 480px)
- Smaller "PITCH MAKER" title at top

**Vertical stepper with 4 steps:**
1. "Writing cinematic script..." (icon: pencil/script)
2. "Generating voiceover..." (icon: microphone)
3. "Creating visuals..." (icon: camera/image)
4. "Assembling final video..." (icon: film)

Each step shows: pending (gray) → in progress (gold, pulsing animation) → completed (green checkmark)

**Polling:** Call `GET /api/status/{jobId}` every 2 seconds. When status is "completed", navigate to Page 3. On error, show error message with "Try Again" button.

### Page 3: Result (route: `/result/:jobId`)

- Full-screen dark background, centered (max-width 800px)
- "Your Pitch is Ready" in gold serif font
- Project name in white below

**Video player:** Full-width 16:9 HTML5 video player with controls. Dark border and shadow.

**Below player:**
- Gold "Download MP4 ↓" button
- Ghost/outline "Create New Pitch →" button (navigates to `/`)

---

## Backend API Specification

### POST /api/generate

**Request:**
```json
{
  "project_name": "string",
  "description": "string",
  "target_audience": "string",
  "key_features": "string",
  "duration_seconds": 30 | 60 | 90,
  "visual_mode": "image" | "video"
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "started"
}
```

Job runs as a background task. Frontend polls status.

### GET /api/status/{job_id}

**Response:**
```json
{
  "job_id": "string",
  "status": "processing" | "completed" | "error",
  "current_step": "generating_script" | "generating_voice" | "generating_visuals" | "assembling_video" | "done",
  "steps": {
    "generating_script": "pending" | "in_progress" | "completed" | "error",
    "generating_voice": "pending" | "in_progress" | "completed" | "error",
    "generating_visuals": "pending" | "in_progress" | "completed" | "error",
    "assembling_video": "pending" | "in_progress" | "completed" | "error"
  },
  "video_url": null | "/api/video/{job_id}/output.mp4",
  "error": null | "error message string"
}
```

### GET /api/video/{job_id}/{filename}

Serves the generated MP4 file. Content-Type: video/mp4.

---

## Pipeline Details

### Step 1: Script Generation (Mistral Large 3)

Call `mistral-large-latest` with JSON response format.

- 30s pitch = 3 scenes
- 60s pitch = 5 scenes
- 90s pitch = 6 scenes

Output schema per scene:
```json
{
  "scene_number": 1,
  "title": "The Challenge",
  "narration": "In a world where brilliant developers...",
  "visual_prompt": "A developer working late, cinematic lighting...",
  "duration_seconds": 12
}
```

Sum of all scene durations must equal total pitch duration.
See PROMPTS.md for the complete Mistral prompt.

### Step 2a: Voice Generation (ElevenLabs) — async

1. Concatenate all scene narrations with `<break time="0.8s"/>` between them
2. Call ElevenLabs text-to-speech API
3. Settings: model=`eleven_v3`, stability=0.4, similarity_boost=0.8, style=0.5
4. Save as `narration.mp3` in job directory

### Step 2b: Visual Generation (fal.ai) — async, parallel with 2a

**Image mode:** Generate all scene images in parallel via `asyncio.gather()`
- Model: `fal-ai/flux-pro/v1.1-ultra`
- Append to each visual_prompt: ", cinematic photography, 16:9, dramatic lighting, National Geographic style"
- Resolution: 1920x1080
- Save as `scene_{n}.png`

**Video mode:** Generate clips sequentially (Kling concurrency limits)
- Model: `fal-ai/kling-video/v2.5/standard/text-to-video`
- Duration: 5 seconds per clip
- Save as `scene_{n}.mp4`
- Fallback: if any clip fails, generate an image instead for that scene

### Step 3: Video Assembly (FFmpeg)

**Image mode:**
1. Each image becomes a video segment with Ken Burns effect (slow zoom 100%→110%)
2. Fade transitions (0.5s) between scenes
3. Title text overlay centered on each scene (white text, dark shadow)
4. Narration audio at full volume
5. Background music at 15% volume with fade in/out
6. Output: H.264 MP4, 1920x1080, 30fps

**Video mode:**
1. Trim each clip to scene duration
2. Crossfade transitions between clips
3. Same text overlays, audio mixing, and export as image mode

---

## Job Storage

In-memory dictionary. No database needed for MVP.

Job files stored in `backend/jobs/{job_id}/`:
```
backend/jobs/{job_id}/
├── script.json
├── narration.mp3
├── scene_1.png (or .mp4)
├── scene_2.png
├── ...
└── output.mp4
```

---

## Error Handling

- Mistral fails → return error, suggest retry
- ElevenLabs fails → return error
- fal.ai image fails for one scene → use dark gradient with title text as fallback
- fal.ai Kling video fails → fall back to image for that scene
- FFmpeg fails → return error with stderr
- All errors update job status and are visible via polling

---

## Development Setup

### Backend
```bash
cd backend
uv add fastapi uvicorn httpx mistralai elevenlabs fal-client python-dotenv
uv run uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
bun install
bun run dev
```

### Vite proxy (vite.config.ts)
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### Prerequisites
- Python 3.11+, Node.js 18+, FFmpeg in PATH
- API keys: Mistral, ElevenLabs, fal.ai

---

## V2 Features (NOT in MVP)

- Multiple TTS voice options
- Visual style templates (NatGeo, TED Talk, Product Hunt)
- Upload your own images/logo
- Background music selection
- Script editing before generation
- Conversational agent interface
- User accounts and saved projects
