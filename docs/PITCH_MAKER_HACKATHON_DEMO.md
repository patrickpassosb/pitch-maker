# Pitch Maker Hackathon Demo

## Ready-To-Paste Form Input

Use these exact values in the app form for your live hackathon demo.

**Project Name**

Pitch Maker

**What does it do?**

Pitch Maker is an AI-powered tool that turns project specs into a cinematic pitch video in minutes. It writes a compelling documentary-style script, generates a professional voiceover, creates stunning visuals, and assembles everything into a polished MP4 ready for demo day.

**Who is it for?**

Hackathon teams, indie builders, developers, and founders who need a memorable pitch fast.

**Key Features**

AI script generation with cinematic storytelling
Professional voiceover with ElevenLabs
AI-generated visuals with image or video modes
Automatic MP4 assembly with music, transitions, and overlays
Simple form-based workflow from idea to demo-ready pitch

**Pitch Duration**

60s

**Visual Style**

AI Images

## Recommended Demo Settings

- Use **60s** for the safest live demo
- Use **AI Images** for faster and more reliable generation
- Keep **AI Video** as a feature you can mention if asked

## Fallback Script

If you want a backup script to reference during the hackathon, use this cinematic script based on the example structure in [PROMPTS.md](file:///home/patrickpassos/GitHub/work/pitch-maker/docs/PROMPTS.md#L68-L114).

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

## Short Demo Intro

Use this one-liner before pressing generate:

Pitch Maker turns a simple project description into a cinematic pitch video with AI-generated storytelling, voice, visuals, and final video assembly.
