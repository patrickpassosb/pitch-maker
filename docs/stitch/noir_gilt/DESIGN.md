# Design System Strategy: Pitch Maker

## 1. Overview & Creative North Star: "The Noir Script"
The Creative North Star for this design system is **"The Noir Script."** This aesthetic transcends standard mobile apps by adopting the visual language of high-end film production, luxury screenplay folios, and cinematic title cards. 

To break the "template" look, we move away from rigid, centered grids in favor of **intentional asymmetry**. Large serif headlines should feel "typeset" rather than just "placed," using wide tracking and generous leading. Elements should overlap—a glass-morphic card might bleed off the edge of the screen or sit halfway over a background gradient—to create a sense of depth and motion, as if the UI is a living frame in a film.

## 2. Color & Surface Architecture
This system relies on the interplay of deep shadows and "light-leaks" to guide the user’s eye. 

### The Palette
- **Primary (The Spotlight):** `#f2c062` (Gold) used sparingly for high-intent actions.
- **Surface (The Darkroom):** `#131313` (Base) and `#0e0e0e` (Lowest).
- **Secondary (The Gaffer):** `#dec396` (Muted Amber) for supportive elements.

### The "No-Line" Rule
Sectioning must be achieved through **tonal transitions**, never through 1px solid lines. To separate a header from a body, transition from `surface` to `surface-container-low`. To define a card, use a `surface-container-high` fill against a `surface` background. The eye should perceive a change in "depth," not a structural boundary.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of materials:
1.  **Base Layer:** `surface-dim` (#131313).
2.  **Sectional Layer:** `surface-container-low` (#1c1b1b).
3.  **Interactive Elements:** `surface-container-highest` (#353534).
4.  **Floating Overlays:** Use a semi-transparent `surface-bright` with a 20px Backdrop Blur to create the "Glassmorphism" effect.

### Signature Textures
Apply a subtle linear gradient to main CTAs (e.g., from `primary` #f2c062 to `primary-container` #d4a54a at 135°). This prevents the gold from looking "flat" and gives it a metallic, polished sheen found in award trophies.

## 3. Typography: The Editorial Voice
The typography is a dialogue between the classic authority of a serif and the modern precision of a sans-serif.

*   **The Hero (Noto Serif):** Used for all `display` and `headline` levels. It conveys the "Pitch" aspect—storytelling, history, and prestige. 
    *   *Directorial Note:* For `display-lg`, use tight letter-spacing (-0.02em) to make the gold text feel like a movie title.
*   **The Script (Inter):** Used for `title`, `body`, and `label`. Inter provides the technical clarity required for "Making." 
    *   *Directorial Note:* Use `label-sm` with 10% letter-spacing for category tags to mimic the look of a production slate.

## 4. Elevation & Depth: Tonal Layering
We do not use drop shadows; we use **Ambient Glows** and **Tonal Lift**.

*   **The Layering Principle:** Depth is achieved by "stacking." A `surface-container-lowest` card placed on a `surface-container-low` section creates a natural "sunken" effect, perfect for input fields or secondary content.
*   **Ambient Glows:** For primary floating buttons, use a shadow with a 24px blur, 0px offset, and 8% opacity using the `primary` color (#f2c062). This creates a "bloom" effect similar to a lens flare in a dark scene.
*   **The "Ghost Border" Fallback:** If accessibility requires a stroke (e.g., in a high-glare environment), use the `outline-variant` token at **15% opacity**. It should be felt, not seen.

## 5. Components & Interface Elements

### Buttons
*   **Primary:** A gold gradient (`primary` to `primary-container`) with `on-primary` (#412d00) text. Roundedness: `md` (0.375rem) to maintain a professional, sharp-edged feel.
*   **Secondary (The Glass Button):** Semi-transparent `surface-container-highest` with a `surface-bright` 10% opacity ghost border.
*   **Tertiary:** Purely text-based using `primary-fixed-dim` with `label-md` styling.

### Cards & Lists (The "No Divider" Rule)
*   **Lists:** Forbid the use of divider lines. Instead, use a `2.5` (0.85rem) spacing gap.
*   **Pitch Cards:** Use `surface-container-high`. The top-left corner should feature a high-contrast `display-sm` serif number (e.g., "01") in `primary` at 20% opacity to create an editorial layout.

### Input Fields
*   **Style:** Minimalist. A `surface-container-lowest` background with a bottom-only `outline-variant` (20% opacity). On focus, the bottom border glows with the `primary` color.

### Cinematic Components (Unique to App)
*   **The "Production Slate" Chip:** A selection chip using `surface-container-highest` with `label-sm` text in all-caps, used for status indicators (e.g., "PRE-PRODUCTION", "FILMING").
*   **The Script Blur:** When scrolling content, the top and bottom of the viewport should feature a `surface` to `transparent` gradient mask (3.5rem height) to make content "fade into the shadows."

## 6. Do's and Don'ts

### Do:
*   **Do** use asymmetrical margins (e.g., a wider left margin for titles than for body text) to create a "Director’s Notebook" feel.
*   **Do** use `primary` sparingly. It is a spotlight, not a floodlight.
*   **Do** use `surface-container` tiers to group related items instead of boxes with borders.

### Don't:
*   **Don't** use pure white (#ffffff) for large blocks of text; use `on-surface` (#e5e2e1) to reduce eye strain in the cinematic dark mode.
*   **Don't** use standard "Material" elevation shadows. Only use ambient glows or tonal shifts.
*   **Don't** use `0.25rem` (default) roundedness for everything. Use `none` for decorative containers to add a sense of brutalist architectural strength.