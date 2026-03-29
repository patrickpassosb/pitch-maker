# 🎬 Pitch Maker

**Turn your project specs into a cinematic pitch video in minutes.**

Pitch Maker is an AI-powered tool that generates National Geographic-style pitch videos for hackathon projects. Describe your project, and the AI writes a compelling script, generates cinematic voiceover, creates stunning visuals, and assembles everything into a polished MP4 you can play at any demo.

## How It Works

1. **Fill the form** — Project name, description, audience, key features, duration
2. **AI writes the script** — Mistral Large 3 creates a cinematic narrative
3. **AI generates voice** — ElevenLabs produces a documentary-style voiceover
4. **AI creates visuals** — fal.ai generates cinematic images or video clips
5. **Auto-assembly** — FFmpeg combines everything into a final MP4 with music

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + TypeScript + Vite + Tailwind CSS |
| Backend | Python + FastAPI + asyncio |
| Script AI | Mistral Large 3 |
| Voice AI | ElevenLabs (eleven_v3) |
| Visual AI | fal.ai (Flux Pro for images, Kling for video) |
| Assembly | FFmpeg |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- FFmpeg installed (`brew install ffmpeg` or `apt install ffmpeg`)
- API keys: Mistral, ElevenLabs, fal.ai

### Setup
```bash
# Clone and configure
cp .env.example .env
# Edit .env with your API keys

# Backend
cd backend
uv add fastapi uvicorn httpx mistralai elevenlabs fal-client python-dotenv
uv run uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
bun install
bun run dev
```

Open http://localhost:5173 and create your first pitch!

## Built at

Build with TRAE SOLO Hackathon — São Paulo, March 29, 2026

## License

MIT
