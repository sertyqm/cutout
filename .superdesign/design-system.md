# Cutout design system

## Product

Cutout is a free, browser-based background-removal tool and a computer-vision portfolio project. A visitor uploads one photo, waits for processing, compares the source and the transparent result with a draggable vertical divider, then downloads a PNG.

The site must feel like a focused tool made by an engineer with taste. The product result is the visual proof. Avoid generic AI imagery, fake testimonials, made-up statistics, feature-card clutter, chatbot visuals, neon gradients, oversized glowing effects and dashboards with no purpose.

## Primary page and flow

Desktop-first responsive single-page tool.

1. Restrained top bar: `CUTOUT` wordmark, a minimal moon/sun theme switch, `Open source` link and a small GitHub link.
2. Hero: concise title and a one-sentence explanation. The hero's visual centre is a real before/after comparison panel, not an illustration.
3. Empty state: an uncluttered upload dropzone with a single primary action, file guidance and a small privacy note.
4. Processing state: the image remains visible with an honest progress state. Do not simulate percentage progress.
5. Result state: a vertical before/after slider. The original source is on the left, the transparent output is presented on a subtle checkerboard to the right. The round divider handle has a visible drag affordance and works with mouse, touch and keyboard. A single `Download PNG` button is visually dominant.
6. A narrow explanation row beneath the tool: `Upload`, `Remove`, `Download`. Use real constraints such as supported formats only when connected to the implementation.
7. Small footer: experiment status, model disclosure link and GitHub.

## Audience and job

The audience is someone who needs a simple transparent cutout and someone reviewing a portfolio project. They should understand the product in five seconds and be able to use it without an account, pricing grid or onboarding flow.

## Visual direction

Use a Swiss-inspired, editorially restrained design derived from the `high-contrast-landing-page` style prompt. Keep it practical rather than theatrical.

- Canvas: off-white `#F4F2ED`.
- Ink: near-black `#161616`.
- Secondary ink: `#6E6C67`.
- Lines: `rgba(22, 22, 22, 0.16)`.
- Tool surface: white `#FFFFFF`.
- Success accent only: muted botanical green `#3F6B58`; use it for a completed state, never as a large gradient.
- Fonts: `Inter` or another clean system sans for all body copy. A single heavy geometric sans may be used for headings if it is available; otherwise use `Inter` at 700–800 weight. Do not use handwritten, sci-fi or decorative fonts.
- Type: compact, precise labels in uppercase with modest tracking. Headline is large but no larger than needed for one or two lines. Body copy is clear and short.
- Geometry: 1px borders, 10–14px corner radius, large quiet margins, a maximum content width around 1180px. Avoid glassmorphism.
- Images: only source and result photos. In the empty state, use an abstract checkerboard crop or no image at all.

## Interaction

- Upload dropzone changes border and background slightly on drag-over. No bouncing animation.
- Before/after divider follows pointer movement in a single frame loop. The handle has a fine vertical rule and a circular centre control.
- Keyboard: left and right arrows move the comparison by 2%; Home and End snap to either side.
- Buttons have a 120–180ms colour transition and a 1px to 2px elevation shift at most.
- Respect `prefers-reduced-motion`.

## Content rules

- Use `Remove the background.` as the main message, with no exclamation mark.
- State `Free to use. No account required.` only if it remains true in the implementation.
- Do not promise perfect hair, commercial-service parity, privacy guarantees or unsupported image limits.
- Do not invent processing times, user counts or endorsements.
- UI text must explain action and outcome, not describe the technology in marketing language.

## Required design constraints

- The before/after slider is the main visual object in the result state.
- The download action must be clear and adjacent to the result.
- The site must be usable at 320px width and on a 1440px desktop viewport.
- Use only the colours, typography, spacing and component style defined here. Do not introduce gradients, neon colours, decorative illustrations or extra font families.
