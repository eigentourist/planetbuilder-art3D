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
- Use `textures/example-base-layer-blurred-4k.png` directly as the shared sRGB color field.
- Center-crop the 16:9 color field into each square layer without changing its aspect ratio.
- Darken the sampled color field separately for each layer before baking.
- For cloud01 only, rotate the color-field coordinates +4 degrees around texture center after center-cropping. Do not rotate its alpha-mask coordinates.
- For cloud03 only, apply a low-frequency nonlinear warp to the color-field coordinates after center-cropping. Do not warp its alpha-mask coordinates:
  - four-dimensional Noise Texture
  - W/seed: 23.7
  - scale: 1.6
  - detail: 2.0
  - roughness: 0.45
  - distortion: 0.10
  - center the noise color around zero and use a UV displacement amplitude of 0.018
- Use `textures/example-noise1.png`, `example-noise2.png`, and `example-noise3.png` as the respective broad structural masks for cloud layers 01–03.
- Center-crop each historical 4:3 mask into its square layer without stretching it.
- Drive fine alpha variation with a four-dimensional Noise Texture and an `EASE`-interpolated Color Ramp.
- Multiply the historical mask by the procedural alpha so the historical image controls broad organic structure and the procedural noise supplies restrained internal variation.
- Use a subtly different, nearly isotropic coordinate scale and rotation for every procedural mask.
- Bake each procedural plane separately against transparent film.
- The experiment 001-004 procedural color-ramp density stops are:
  - position 0.43: alpha 0.0
  - position 0.53: alpha 0.10
  - position 0.66: alpha 0.52
  - position 0.82: alpha 0.80
- Remap the cloud01 and cloud02 historical masks through a higher-contrast `EASE` ramp with these stops:
  - position 0.16: value 0.0
  - position 0.42: value 0.10
  - position 0.68: value 0.90
  - position 0.90: value 1.0
- For cloud03, retain `B_SPLINE` interpolation while increasing contrast:
  - position 0.12: value 0.0
  - position 0.38: value 0.12
  - position 0.72: value 0.90
  - position 0.94: value 1.0
- After contrast adjustment, approximate a conservative spatial alpha blur with five mask samples:
  - center sample at weight 0.40
  - left, right, up, and down samples at weight 0.15 each
  - offset cardinal samples by 0.006 UV units, approximately 12 pixels at 2048×2048
- Blur only the historical-mask contribution before multiplying it by procedural alpha. Do not blur RGB color data.
- Keep overall exposure dark, distribute clouds rather than filling the frame, and retain quieter negative space behind the centered logo.
- Favor diffuse forms. Occasional filament-like forms must also remain soft and ephemeral.

### Cloud 01 — broad horizontal

- Noise seed/W: 2.3
- Scale: 3.2
- Detail: 4.5
- Roughness: 0.66
- Distortion: 0.30
- Mapping scale: `(0.92, 1.08, 1.0)`
- Mapping rotation: −12 degrees
- Color-field value multiplier: 0.59
- Historical structural mask: `textures/example-noise1.png`
- Composite rotation: −8 degrees
- Composite offset: `(-2.8, 1.7)`
- Composite scale: `(1.20, 1.15)`
- Suggested Godot rotation speed: +0.16 degrees per second

### Cloud 02 — diagonal

- Noise seed/W: 9.1
- Scale: 3.6
- Detail: 5.2
- Roughness: 0.70
- Distortion: 0.42
- Mapping scale: `(1.08, 0.92, 1.0)`
- Mapping rotation: +31 degrees
- Color-field value multiplier: 0.55
- Historical structural mask: `textures/example-noise2.png`
- Composite rotation: +11 degrees
- Composite offset: `(2.8, -1.8)`
- Composite scale: `(1.24, 1.17)`
- Suggested Godot rotation speed: −0.12 degrees per second

### Cloud 03 — diffuse filaments

- Noise seed/W: 16.7
- Scale: 4.2
- Detail: 3.0
- Roughness: 0.56
- Distortion: 0.78
- Mapping scale: `(0.82, 1.18, 1.0)`
- Mapping rotation: −38 degrees
- Color-field value multiplier: 0.66
- Historical structural mask: `textures/example-noise3.png`
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

Experiment 001-001 established the pipeline, but its alpha coverage and brightness produced a field that was too solid and uniform. Experiment 001-002 introduced the 4K color field, high-contrast masks, anisotropic mapping, and true black separation, but was too dark and band-like. Experiment 001-003 broadened and softened the masks and improved visibility, although horizontal banding remained in the lower-right amber cloud. Experiment 001-004 uses the historical production noise images for broad structure and restrained procedural noise for internal variation, resolving most of the regular banding while preserving a dark central region. Experiment 001-005 changes only the shared color source to the blurred 4K variant, smoothing broad color transitions without eliminating useful cloud texture. Experiment 001-006 gives cloud03 a gentler historical-mask remap, but confirms that its colored circular contour primarily originates in the blurred color field. Experiment 001-007 applies higher contrast followed by a conservative five-tap blur to all three historical masks, producing cleaner dark separation while retaining diffuse edges. Experiment 001-008 rotates only cloud01's color coordinates by +4 degrees to disrupt the marked upper-left parallelogram-like contour; the contour becomes slightly less coherent but persists. Experiment 001-009 retains that rotation and adds a subtle low-frequency nonlinear warp to cloud03's color coordinates. The warp safely bends cloud03's color transitions but is too subtle to remove the marked composite contour.
