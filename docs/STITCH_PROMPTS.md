# Pitch Maker — Google Stitch Design Prompts

Use these prompts in Google Stitch (stitch.withgoogle.com) to generate
the 3 pages of the Pitch Maker UI. Export the screenshots and save them
in your docs/design/ folder.

---

## Stitch Prompt for All 3 Screens

Paste this into Stitch to generate all pages at once:

```
Design a 3-screen web application called "Pitch Maker" with a dark, 
cinematic movie studio aesthetic.

Theme: Deep black backgrounds (#0a0a0a), subtle dark gradients, 
gold/amber accent color (#d4a54a), white text. Think movie studio 
or film production app. Use a serif font for the logo/headings 
(like Playfair Display) and a clean sans-serif for body text (like Inter).

Screen 1 — Input Form:
- Full-screen dark background with subtle radial gradient from center
- Centered card (max-width 640px) with a glass-morphism effect
- Logo at top: "PITCH MAKER" in large gold serif letters with a subtle glow effect
- Subtitle below: "Turn your project into a cinematic pitch" in gray
- Form with 6 fields, all with dark input backgrounds and subtle borders:
  1. "Project Name" — text input
  2. "What does it do?" — textarea, 3 rows
  3. "Who is it for?" — text input  
  4. "Key Features" — textarea, 4 rows
  5. "Pitch Duration" — 3 toggle buttons in a row: 30s, 60s, 90s
  6. "Visual Style" — toggle switch between "AI Images" and "AI Video Clips"
- Large gold gradient submit button: "Generate Cinematic Pitch →"

Screen 2 — Generating Progress:
- Full-screen dark background
- Centered content (max-width 480px)
- Smaller "PITCH MAKER" logo at top
- Vertical stepper showing 4 steps with connecting lines:
  1. "Writing cinematic script..." (completed, green check)
  2. "Generating voiceover..." (in progress, gold pulsing)
  3. "Creating visuals..." (pending, gray)
  4. "Assembling final video..." (pending, gray)
- Each step has an icon, title, and status indicator
- Subtle film grain or particle animation in background

Screen 3 — Result:
- Full-screen dark background
- Centered (max-width 800px)
- "Your Pitch is Ready" in gold serif font at top
- Project name below in white
- Large 16:9 video player with dark border and shadow
- Below the player: gold "Download MP4" button and outline "Create New Pitch" button
- Small stats line: "Duration: 60s • 5 scenes • Generated in 28s"
```

---

## Individual Screen Prompts (if generating one at a time)

### Screen 1 Only:
```
Design a dark, cinematic input form for an app called "Pitch Maker". 
Deep black background (#0a0a0a) with gold accents (#d4a54a). 
Centered glass-morphism card. Logo "PITCH MAKER" in gold serif font 
at top. Form fields: Project Name, What does it do (textarea), 
Who is it for, Key Features (textarea), Pitch Duration (30s/60s/90s 
toggle buttons), Visual Style (toggle: AI Images / AI Video Clips). 
Large gold gradient submit button. Movie studio aesthetic.
```

### Screen 2 Only:
```
Design a dark, cinematic progress/loading screen for "Pitch Maker". 
Deep black background, centered content. Small logo at top. 
Vertical stepper with 4 steps connected by lines: "Writing cinematic 
script" (done, green check), "Generating voiceover" (in progress, 
gold pulsing glow), "Creating visuals" (pending, gray), "Assembling 
final video" (pending, gray). Each step has an icon and status text. 
Film production aesthetic with gold accents.
```

### Screen 3 Only:
```
Design a dark, cinematic result page for "Pitch Maker". Deep black 
background. "Your Pitch is Ready" heading in gold serif font. 
Large 16:9 video player in the center with dark borders and glow 
effect. Below the player: gold "Download MP4" button and a ghost 
outline "Create New Pitch" button. Small stats: "Duration: 60s • 
5 scenes • Generated in 28s". Premium movie studio feel.
```
