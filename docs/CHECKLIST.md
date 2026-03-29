# Pitch Maker — Pre-Hackathon Preparation Checklist

## Tonight (March 28) — Preparation

### Documents (done!)
- [ ] Save SPEC.md to local folder
- [ ] Save ARCHITECTURE.md to local folder
- [ ] Save PROMPTS.md to local folder
- [ ] Save .env.example to local folder
- [ ] Save README.md to local folder
- [ ] Save .gitignore to local folder
- [ ] Save STITCH_PROMPTS.md to local folder

### UI Design
- [ ] Go to stitch.withgoogle.com
- [ ] Generate the 3 screens using prompts from STITCH_PROMPTS.md
- [ ] Export/screenshot each screen
- [ ] Save screenshots to local folder as:
  - page1-input.png
  - page2-generating.png
  - page3-result.png

### API Keys — Test Each One
- [ ] **Mistral AI**: Go to console.mistral.ai → API Keys → Create key
  - Test: Open terminal, run a quick curl or Python script to verify
- [ ] **ElevenLabs**: Go to elevenlabs.io → Settings → API Keys
  - Test: Generate one sentence of audio to verify key works
- [ ] **fal.ai**: Go to fal.ai → Sign up → Dashboard → Keys
  - Test: Generate one image to verify key works and see how credits work
- [ ] Save all keys somewhere safe (password manager, not in a file)

### ElevenLabs Voice
- [ ] Browse https://elevenlabs.io/voice-library
- [ ] Filter by "Cinematic" category
- [ ] Preview 5-10 voices, pick the most National Geographic one
- [ ] Copy the Voice ID (long string like "JBFqnCBsd6RMkjVDRZzb")
- [ ] Save the Voice ID with your API keys

### Background Music
- [ ] Go to YouTube Audio Library (studio.youtube.com → Audio Library)
  - OR Pixabay Music (pixabay.com/music)
  - OR Free Music Archive
- [ ] Search for: "cinematic", "documentary", "epic", "inspirational"
- [ ] Download ONE track, ~90 seconds, no vocals
- [ ] Save as background.mp3 in local folder
- [ ] Make sure it's royalty-free!

### TRAE IDE
- [ ] Download and install TRAE from trae.ai
- [ ] Create account
- [ ] Familiarize yourself with SOLO Builder mode
- [ ] Test that it works by creating a simple project

### Environment
- [ ] Verify Python 3.11+ is installed: `python --version`
- [ ] Verify Node.js 18+ is installed: `node --version`
- [ ] Verify FFmpeg is installed: `ffmpeg -version`
  - If not: `brew install ffmpeg` (Mac) or download from ffmpeg.org
- [ ] Verify uv works: `uv --version`
- [ ] Verify bun works: `bun --version`

---

## Morning of March 29 — Before the Event

- [ ] Charge your laptop fully
- [ ] Double-check all API keys still work (quick test call each)
- [ ] Have your local docs folder ready and accessible
- [ ] Have your .env values ready to copy-paste
- [ ] Have the background.mp3 file ready
- [ ] Have the Stitch screenshots ready
- [ ] Open the SPEC.md file so you can copy-paste it quickly

---

## At the Hackathon — Execution Plan

### 0:00 - 0:05 — Setup
- [ ] Create GitHub repo "pitch-maker" (public)
- [ ] Open TRAE SOLO
- [ ] Paste the FULL SPEC.md into TRAE
- [ ] Say: "Build this project following this specification exactly"

### 0:05 - 0:30 — TRAE Scaffolds + Fix Issues
- [ ] Let TRAE generate the project structure
- [ ] Copy .env with your real API keys
- [ ] Copy background.mp3 to assets/music/
- [ ] Fix any import errors or missing dependencies
- [ ] Get both frontend and backend running

### 0:30 - 1:00 — Pipeline Integration
- [ ] Test Step 1: Mistral script generation alone
- [ ] Test Step 2a: ElevenLabs voice generation alone
- [ ] Test Step 2b: fal.ai image generation alone
- [ ] Test Step 3: FFmpeg assembly with hardcoded inputs

### 1:00 - 1:30 — End-to-End Testing
- [ ] Run the full pipeline start to finish
- [ ] Fix any bugs
- [ ] Test with both "AI Images" and "AI Video Clips" modes

### 1:30 - 1:45 — Demo Prep
- [ ] Generate a complete pitch video for "Pitch Maker" (your demo video)
- [ ] Save this video — this is your safety net for the demo
- [ ] Test the download button works

### 1:45 - 2:00 — Polish
- [ ] UI touch-ups if needed
- [ ] Push all code to GitHub
- [ ] Prepare what you'll say during the demo

---

## Demo Strategy

1. Start by playing the pre-generated pitch video for "Pitch Maker"
   - This shows what the output looks like (impressive cinematic video)

2. Then do a live generation with a different project
   - Use a simple fake project so the form is quick to fill
   - Select "AI Images" mode (fast, reliable)
   - Show the progress steps happening in real-time

3. While it generates, explain:
   - "It's using Mistral AI to write the script"
   - "ElevenLabs is generating the voiceover"
   - "fal.ai is creating cinematic images"
   - "FFmpeg is assembling everything into a video"

4. When the video is ready, play it live

5. If asked about the video mode, explain it also supports AI video clips
   via Kling — show that the toggle exists
