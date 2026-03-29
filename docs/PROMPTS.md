# Pitch Maker — Prompt Templates

## Mistral System Prompt (Script Generation)

This is the system prompt for Mistral Large 3. It instructs the model to generate a structured cinematic pitch script.

```
You are a world-class pitch writer and documentary filmmaker who creates compelling, cinematic narrations in the style of National Geographic documentaries. Your writing is vivid, dramatic, and emotionally engaging — it makes the audience feel the importance of what they're watching.

Your task is to generate a structured pitch script for a hackathon project. The script will be used to generate:
1. A cinematic voiceover narration (read by a professional narrator)
2. AI-generated visuals for each scene
3. On-screen title text for each scene

RULES:
- Write in English
- Use a dramatic, documentary-style tone — think National Geographic, Planet Earth, or a TED talk opening
- Create a narrative arc: hook the audience → present the problem → introduce the solution → showcase features → end with a powerful vision
- Each scene's narration should be 2-4 sentences, meant to be spoken aloud
- Each visual_prompt should describe a cinematic, photographic image that could illustrate the narration
- Visual prompts should be detailed: describe lighting, mood, camera angle, composition
- The title for each scene should be 1-4 words that capture the scene's theme
- The sum of all scene duration_seconds MUST exactly equal total_duration_seconds
- Scene durations should roughly match the narration length (longer narrations = more seconds)

OUTPUT FORMAT:
Respond ONLY with a valid JSON object matching this exact schema. No markdown, no explanation, just JSON:

{
  "title": "Project Name",
  "total_duration_seconds": <number>,
  "scenes": [
    {
      "scene_number": 1,
      "title": "Short Title",
      "narration": "The narration text spoken by the voiceover narrator...",
      "visual_prompt": "Detailed description of the cinematic image or video for this scene...",
      "duration_seconds": <number>
    }
  ]
}
```

## Mistral User Prompt Template

```
Generate a cinematic pitch for this project:

Project Name: {project_name}
Description: {description}
Target Audience: {target_audience}
Key Features:
{key_features}

Total Duration: {duration_seconds} seconds
Number of scenes: {num_scenes}

Create exactly {num_scenes} scenes. The sum of all scene durations must equal exactly {duration_seconds} seconds.
```

### Scene Count by Duration:
- 30 seconds → 3 scenes (10s each approximately)
- 60 seconds → 5 scenes (12s each approximately)
- 90 seconds → 6 scenes (15s each approximately)

---

## Example Output (60-second pitch for Pitch Maker)

This is what the Mistral response should look like. Use this as a reference to validate the output format.

```json
{
  "title": "Pitch Maker",
  "total_duration_seconds": 60,
  "scenes": [
    {
      "scene_number": 1,
      "title": "The Silent Struggle",
      "narration": "Every year, thousands of developers pour their brilliance into hackathon projects. They build tools that could change industries. Yet when the clock strikes demo time, their ideas die — not because the code wasn't good enough, but because the pitch fell flat.",
      "visual_prompt": "A lone developer sitting at a desk late at night, surrounded by multiple glowing monitors showing code. The room is dark except for the blue light of screens. Cinematic side lighting, shallow depth of field, moody atmosphere. Shot from a low angle looking up at the developer's concentrated face.",
      "duration_seconds": 14
    },
    {
      "scene_number": 2,
      "title": "A New Era",
      "narration": "What if you could transform your project specs into a cinematic masterpiece? What if your pitch could rival the production quality of a National Geographic documentary — generated in seconds, not days?",
      "visual_prompt": "A dramatic transformation scene: a simple text document morphing into a beautiful cinematic video playing on a large screen. Golden light rays emanating from the screen. Futuristic, clean workspace with dramatic volumetric lighting. Wide angle shot showing the scale of the transformation.",
      "duration_seconds": 12
    },
    {
      "scene_number": 3,
      "title": "Introducing Pitch Maker",
      "narration": "Introducing Pitch Maker. Simply describe your project — what it does, who it serves, why it matters. Our AI engine crafts a compelling narrative, generates a cinematic voiceover, and creates stunning visuals. All assembled into a professional video you can play at any demo.",
      "visual_prompt": "A sleek, modern dark interface showing the Pitch Maker application. A form is being filled out and a beautiful progress animation shows the AI working. The screen glows with golden amber accents against a deep black background. Product photography style, sharp focus, premium feel.",
      "duration_seconds": 14
    },
    {
      "scene_number": 4,
      "title": "The Technology",
      "narration": "Powered by Mistral AI for scriptwriting, ElevenLabs for voice synthesis, and cutting-edge image generation, Pitch Maker orchestrates an entire production studio — in your browser. From concept to cinema in under a minute.",
      "visual_prompt": "Abstract visualization of AI neural networks connecting different creative elements: text flowing into sound waves, sound waves connecting to cinematic images, images assembling into a film reel. Dark background with glowing connections in gold and blue. Futuristic data visualization style, clean and elegant.",
      "duration_seconds": 12
    },
    {
      "scene_number": 5,
      "title": "Your Story Awaits",
      "narration": "Your code deserves more than a rushed live demo. It deserves a story. It deserves cinema. Pitch Maker — because every great project deserves a great pitch.",
      "visual_prompt": "A packed hackathon audience watching a massive screen where a cinematic pitch video is playing. The audience is captivated, faces lit by the warm glow of the screen. Shot from behind the audience looking toward the stage. Epic, wide cinematic composition with dramatic lighting and a sense of awe.",
      "duration_seconds": 8
    }
  ]
}
```

---

## Visual Prompt Enhancement

Before sending any `visual_prompt` to fal.ai, append this suffix to improve cinematic quality:

```
, cinematic photography, 16:9 aspect ratio, high detail, dramatic lighting, National Geographic documentary style, professional color grading, shallow depth of field
```

This ensures consistent visual quality across all scenes regardless of what Mistral generates.

---

## ElevenLabs Voice Selection Guide

When choosing a voice from the ElevenLabs library for the cinematic narrator:

**Search for:** "cinematic" or "documentary" or "narrator" in the voice library

**Ideal voice characteristics:**
- Deep, resonant male or female voice
- Clear enunciation
- Natural dramatic pauses
- Warm but authoritative tone
- Think: David Attenborough, Morgan Freeman, or a National Geographic narrator

**Voice settings for cinematic output:**
- stability: 0.4 (lower = more dramatic variation)
- similarity_boost: 0.8 (higher = more consistent to the chosen voice)
- style: 0.5 (moderate expressiveness)
- use_speaker_boost: true

**Browse the cinematic voices at:** https://elevenlabs.io/voice-library
Filter by "Cinematic" category and preview several before picking one.
Save the voice_id for your .env file.
