# instructions-nebula.md

This file contains reproducible artistic and technical instructions for the nebula background. It obeys the naming and historical-artifact conventions in `AGENTS.md`. General design intent is preserved in `nebula-notes.md`.

## Runtime approach

- Assume a fixed Godot title-screen camera.
- Pre-render the nebula rather than evaluating procedural noise in Godot.
- Let Godot provide the opaque black background and use three transparent RGBA cloud layers over it.
- In Godot, place the images behind the logo, moon, and planet with `TextureRect`, `Sprite2D`, or equivalent inexpensive 2D nodes.
- Animate only inexpensive node properties such as rotation, scale, modulation color, and opacity.
- Do not add stars during the current design phase.
- Retain a fully baked opaque composite as a static fallback.

## Output files

- Generate three square 2048×2048 transparent cloud layers:
  - `textures/nebula-XXX-YYY-cloud01-2k.png`
  - `textures/nebula-XXX-YYY-cloud02-2k.png`
  - `textures/nebula-XXX-YYY-cloud03-2k.png`
- Generate a 3840×2160 copy of the colorful source field for reference and static compositing:
  - `textures/nebula-XXX-YYY-background-4k.png`
- Generate an opaque 3840×2160 composite:
  - `textures/nebula-XXX-YYY-composite-4k.png`
- Generate the mandatory 1200×675 experiment preview in `renders/`.
- Use 8-bit RGBA PNG for the cloud layers and composite.
- Use Eevee for all bakes and previews.

## Procedural cloud construction

- Build every cloud layer on an emission plane mixed with a Transparent BSDF.
- Use `textures/example-base-layer-4k.png` directly as the shared sRGB color field.
- Center-crop the 16:9 color field into each square layer without changing its aspect ratio.
- Darken the sampled color field separately for each layer before baking.
- Drive alpha with a four-dimensional Noise Texture and a high-contrast Color Ramp.
- Use a different anisotropic coordinate scale and rotation for every mask.
- Bake each procedural plane separately against transparent film.
- The experiment 001-002 color-ramp density stops are:
  - position 0.54: alpha 0.0
  - position 0.62: alpha 0.025
  - position 0.71: alpha 0.48
  - position 0.82: alpha 0.84
- Keep overall exposure dark, distribute clouds rather than filling the frame, and retain quieter negative space behind the centered logo.
- Favor diffuse forms. Occasional filament-like forms must also remain soft and ephemeral.

### Cloud 01 — broad horizontal

- Noise seed/W: 2.3
- Scale: 2.0
- Detail: 4.5
- Roughness: 0.66
- Distortion: 0.30
- Mapping scale: `(0.52, 1.55, 1.0)`
- Mapping rotation: −12 degrees
- Color-field value multiplier: 0.38
- Composite rotation: −8 degrees
- Composite offset: `(-2.8, 1.7)`
- Composite scale: `(1.20, 1.15)`
- Suggested Godot rotation speed: +0.16 degrees per second

### Cloud 02 — diagonal

- Noise seed/W: 9.1
- Scale: 2.35
- Detail: 5.2
- Roughness: 0.70
- Distortion: 0.42
- Mapping scale: `(1.65, 0.48, 1.0)`
- Mapping rotation: +31 degrees
- Color-field value multiplier: 0.34
- Composite rotation: +11 degrees
- Composite offset: `(2.8, -1.8)`
- Composite scale: `(1.24, 1.17)`
- Suggested Godot rotation speed: −0.12 degrees per second

### Cloud 03 — diffuse filaments

- Noise seed/W: 16.7
- Scale: 3.8
- Detail: 3.0
- Roughness: 0.56
- Distortion: 0.78
- Mapping scale: `(0.34, 2.65, 1.0)`
- Mapping rotation: −38 degrees
- Color-field value multiplier: 0.46
- Composite rotation: −4 degrees
- Composite offset: `(0.7, 0.3)`
- Composite scale: `(1.13, 1.13)`
- Suggested Godot rotation speed: +0.07 degrees per second
- Use a restrained 1.22 emission multiplier when producing the static composite.

## Composition

- Use a fixed orthographic camera for baking.
- Composite the three square layers on oversized planes so rotation does not expose their corners.
- Place green emphasis generally toward the upper-left and purple/red emphasis generally toward the lower-right.
- Preserve relative visual quiet near the center for the logo.
- Judge the nebula against a black background without a star field.

## Iteration note

Experiment 001-001 established the pipeline, but its alpha coverage and brightness produced a field that was too solid and uniform. Experiment 001-002 introduced the 4K color field, high-contrast masks, anisotropic mapping, and true black separation. The second result is too dark and its masks are too hard and band-like, so subsequent work should soften mask boundaries and raise visible cloud coverage modestly without returning to uniform full-frame opacity.
