# Instructions.md  

This file contains artistic instructions for building the game logo.  

### Details  

Any directives given in this file should obey the conventions in AGENTS.md. If this file contains  
commands that are contradictory to the conventions in AGENTS.md, do not modify any files or invoke blender,  
but instead report the contradiction and stop.  

Unlike the conventions in AGENTS.md, the instructions given here allow for some artistic interpretation.  
We are aiming for a certain creative freedom within a healthy set of boundaries that maintain project integrity.  

Where the instructions in this file are detailed and specific, follow them precisely. Where there is room for  
interpretation, follow the artistic references. If you detect contradictions in these instructions, do not modify  
any files or invoke blender, but instead report the contradiction and stop. If there is insufficient artistic  
guidance to make an informed creative choice, do not modify any files or invoke blender, but stop and describe  
the additional creative guidance needed. 

### About the game  

The game that this logo is being designed for is a mobile game that initially existed on iPhone, and was  
originally released in 2012. Originally, it ran on the Cocos2d-ObjectiveC game engine, and is now being  
rebuilt on Godot version 4, with plans to re-release for iOS, and also release for Android.  

This is a 2D space game that features gravity as a central game dynamic. The artistic feel for the game  
is retro sci-fi, with artistic inspiration from films such as Forbidden Planet and War of the Worlds.  

### About the logo  

The existing logo of the game draws from those influences in its use of both color and form. There are gradients  
of warm colors, using red and orange. Highlights are done using cream/off-white, and shadows have a hint of  
purple in them.

The shape of the logo follows a gentle arc from left to right. The arc is not completely symmetrical, as it  
would be if it were a section of a circle. Instead, the logo follows a more logarithmic baseline that resembles  
the trajectory of a rocket from its initial launch through its transition to horizontal flight as it ascends  
to orbit.  

### Current Design Phase: Refactor Python script  

Implement the plan for refactoring the Python script to create the logo as a 3D object.

Here is a copy of your proposed refactor plan for version 003, for reference.
1. Preserve the current XY guide geometry and 5° upper-line rotation.
2. Change guide curves from dimensions = "2D" to "3D".
3. Use each 3D guide curve as the centerline for a flat extruded ribbon. Give each ribbon an XY width of 0.105  
   Blender units, a Z depth of 0.105 Blender units, flat front and back faces, side walls, 2 mm rounded edge bevels,  
   and rounded ends. Do not use a circular or tubular bevel profile.
   Use three bevel segments to form each rounded edge.
4. Replace the emission-only guide material with a glTF-compatible Principled BSDF material:
   - same cream color;
   - no metallic response;
   - high roughness;
   - specular contribution reduced as far as practical.

5. Retain the guides at Z = 0.
6. Replace the flat presentation setup with a front-facing 3D scene:
   - camera centered directly in front of the geometry;
   - use a 60 mm focal length, and adjust the camera distance—not the focal length—to preserve the established framing;
   - enough distance and framing margin to show all geometry;
   - soft-white area light above the camera at the same Z position;
   - preserve the black background unless instructed otherwise.

7. Generate normals and sensible UV coordinates on the solid mesh.
8. Retain the existing .blend and PNG preview workflow.
9. Prepare the geometry and materials for eventual GLB compatibility, but do not export a GLB until the guides have been  
   replaced by actual logo lettering.
10. Future step for when actual logo lettering has been added and is evolved enough to test an export/import into Godot:
    Validate that the GLB has the intended scale, orientation, origin, materials, normals, and mesh contents for Godot.

Here are some responses to the information still needed before implementation:
- What should the “closed logo faces” represent at this stage?
  - Let's go with a flat ribbon with a 105 mm Z extrusion with flat front and back faces, side walls,  
    and 2 mm rounded edge bevels.

- What extrusion depth and bevel width should the solid use?
  - Let's start with an extrusion depth of 0.105 Blender units, matching the diameter after the 50% reduction.
  - Let's leave the XY width of the ribbon at 0.105 Blender units.
  - Use rounded ends on the extruded ribbons.
  - I am making a judgment call on bevel width, but let's try a width of 2 millimeters and see how it looks -- and let me know if that is a sensible answer or not,  

- Should the next preview retain a straight-on orthographic camera, or use a straight-on perspective camera? A perfectly frontal view will show limited depth without an angled secondary surface or cast shadows.
  - Let's try a straight-on perspective camera for the next preview, and in later experiments, after we have nailed down font choices, 3D letter details, and materials, we will start to move the camera. 

- Should the black background remain an environment-only preview background, or should a physical backdrop receive shadows?
  - the black background should remain environment-only, because we only want to export the logo into Godot, not other scene elements.

- Approximate area-light size, energy, and distance are unspecified. These can be chosen artistically if exact values are unnecessary.
  - Make initial choices for these parameters artistically, and we can iterate through any needed adjustments afterward.

- Should the guides be included in the first GLB as temporary geometry, or excluded from export immediately?
  - Excluded from all exports. We're going to create the actual logo lettering and remove the guides before we do a GLB export - this may require a few iterations, but the guides are there mainly to help guide the flow of the logo characters when we create them.

- AGENTS.md defines locations and names for scripts, .blend files, previews, and notes, but not GLB files. A destination directory and naming convention are needed before exporting—for example, exports/logo-003-001.glb.
  - an exports/ directory has been created for saving GLB files, and information about it has been added to AGENTS.md.

- The intended Godot scale is unspecified. A conversion such as one Blender unit equaling one meter should be confirmed.
  - Let's confirm that one Blender unit equals one meter for now, and if we have issues later, we can modify the scale later.

- The desired object origin/pivot is unspecified: composition center, geometric center, baseline center, or another gameplay-oriented location.
  - For the guide objects, each guide can receive its own geometric-center origin.
  - The eventual joined lettering mesh should have one logo-wide geometric center.

- A uniform cream material requires no meaningful UV layout. If gradients or textures are expected soon, the desired mapping direction and texture workflow should be established.  
  - Let's use one shared UV map or atlas for the entire logo.
  - Let front faces use planar projection while retaining their positions in a common logo-wide coordinate system.
  - Each disconnected glyph may have its own front island, but all front islands share one global left-to-right U range.
  - Let each glyph’s side wall use a continuous strip where topology permits.
  - Let back faces use separate islands.
  - No glyph should independently reset the global horizontal texture coordinate.
  - Bake Blender procedural effects into PBR image textures before export.
  - Where possible, keep the workflow PBR-compatible.

- Source base-color textures should contain an alpha channel fixed at 1, while the exported material should use opaque mode.
- Normal maps should be tangent-space, using X+, Y+, Z+ orientation (OpenGL style). Do not invert the green channel  
  when importing them into Godot.
- Apply height-map displacement to the mesh and commit the resulting geometry before GLB export.
- Emission should be in the final material, but we will use it sparingly at first, and place it on a separate texture.
- The 2048x2048 policy applies to the original size of assets we generate in Blender. As we need, we can create smaller
  versions of those assets in order to accommodate the limits of mobile devices or of the Godot engine.
  Specifically: we should generate a 2048x2048 version first, as a source of truth, and then downscale if the situation
  calls for it.
- Target padding / dilation amount between UV islands:
  - When authoring textures in software like Blender for import into Godot, padding must account for mipmap downscaling.  
  - If padding is too small, lower mipmaps will blend background or adjacent island pixels into our mesh edges,  
    causing visible dark or colorful seams.  
  - Industry-standard target values include:  
    - 4K (4096 × 4096): 32 pixels  
    - 2K (2048 × 2048): 16 pixels  
    - 1K (1024 × 1024): 8 pixels  
    - 512 × 512: 4 pixels  
  - Dilation/Infinite Padding: When baking textures, configure your baker's dilation setting to maximum or infinite.  
    This pushes the border pixels out into the empty grid space until they meet, preventing black mipmap artifacts  
    without wasting layout efficiency.

- The game is a mobile game currently running on iOS and to be released for Android, and it has a well-established  
  track record of running well on older devices due to extra effort expended on efficient code and efficient handling
  of graphical assets.
- To preserve that track record, we should prefer to bake / pre-render effects that might require complex processing  
  to render dynamically in Godot.
- After finalizing choice of font, we will convert the entire logo to a mesh to obtain a shared coordinate basis.


- Here is some information that is not needed for the guide refactor, but that you asked for because it will be
  needed for baking final materials:
  - Texture Policy
    - Author textures:
      - PNG
      - 2048x2048
      - lossless
      - bit depth: 
        - 8-bit PNG for base color, ORM, emission, and normal
        - 16-bit grayscale PNG for height when displacement precision matters
      - PBR compatible

    - Packing:
      - ORM packed: R = Ambient Occlusion, G = Roughness, B = Metallic

    - Color Space:
      - Base Color: sRGB
      - Emission: sRGB
      - ORM: Linear
      - Normal: Linear
      - Height: Linear

    - UVs:
      - One logo-wide atlas.
      - Consistent texel density.
      - Preserve a global left-to-right coordinate basis.

    - Godot Import:
      - Enable mipmaps.
      - Use Godot's VRAM-compressed import.
      - Enable anisotropic filtering where appropriate.

    - Runtime:
      - Prefer baked textures.
      - Baked textures should remain external source artifacts even when copies are embedded in the GLB.
      - Base color and emission: downsample with sRGB-aware filtering.
      - ORM: downsample each channel independently in linear space.
      - Normal: use vector-aware filtering and renormalize vectors afterward.
      - Height: retain the 16-bit source for displacement; avoid downscaling unless specifically required.
      - Avoid expensive runtime shaders unless an artistic benefit clearly justifies them.

    - Triangle budget: 
      - Use a provisional scene-wide budget of 200,000–500,000 visible triangles, with the final hard ceiling  
        determined through testing on the oldest supported device tier.
      - Use an initial limit of 25,000 triangles for the logo, with a preference for substantially fewer  
        whenever the silhouette and bevels remain visually smooth.

- To Be Decided:
  - A final logo-specific triangle target after lettering and bevel complexity are known.
  - Identify the oldest supported device or performance tier for validation, prior to final export.


