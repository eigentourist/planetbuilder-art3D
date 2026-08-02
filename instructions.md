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

### Current Design Phase: Plan refactor of Python script  

Describe a plan for refactoring the Python script to create the logo as a 3D object.

Here is a copy of your proposed refactor plan for version 003, for reference.
1. Preserve the current XY guide geometry and 5° upper-line rotation.
2. Change guide curves from dimensions = "2D" to "3D".
3. Explicitly set full curve fill behavior while retaining bevel depth, bevel resolution, and capped ends.
4. Replace the emission-only guide material with a glTF-compatible Principled BSDF material:
   - same cream color;
   - no metallic response;
   - high roughness;
   - specular contribution reduced as far as practical.

5. Retain the guides at Z = 0.
6. Replace the flat presentation setup with a front-facing 3D scene:
   - camera centered directly in front of the geometry;
   - enough distance and framing margin to show all geometry;
   - soft-white area light above the camera at the same Z position;
   - preserve the black background unless instructed otherwise.

7. Add closed face geometry separately from the temporary guides. Extrude it along Z and add modest beveling so the front, back, and side surfaces read as a solid object.
8. Generate normals and sensible UV coordinates on the solid mesh.
9. Retain the existing .blend and PNG preview workflow.
10. Add GLB export after saving and rendering:
    - convert exportable curve or face geometry to meshes;
    - apply transforms;
    - export only intended logo geometry;
    - exclude camera, lighting, and temporary guides unless requested;
    - use Blender’s glTF exporter with export_format="GLB".

11. Validate that the GLB has the intended scale, orientation, origin, materials, normals, and mesh contents for Godot.

Here are some responses to the information still needed before implementation:
- What should the “closed logo faces” represent at this stage?
  - Let's go with an extruded round ribbon for now.

- What extrusion depth and bevel width should the solid use?
  - Let's start with an extrusion depth of 0.105 Blender units, matching the diameter after the 50% reduction..
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
  - Let's begin with geometric center for now, and if necessary, we can change to another origin/pivot later.

- A uniform cream material requires no meaningful UV layout. If gradients or textures are expected soon, the desired mapping direction and texture workflow should be established.  
  - Let's use one shared UV map or atlas for the entire logo.
  - Let front faces use planar projection while retaining their positions in a common logo-wide coordinate system.
  - Each disconnected glyph may have its own front island, but all front islands share one global left-to-right U range.
  - Let each glyph’s side wall use a continuous strip where topology permits.
  - Let back faces use separate islands.
  - No glyph should independently reset the global horizontal texture coordinate.
  - Bake Blender procedural effects into PBR image textures before export.
  - Where possible, keep the workflow PBR-compatible.

- The game is a mobile game currently running on iOS and to be released for Android, and it has a well-established  
  track record of running well on older devices due to extra effort expended on efficient code and efficient handling
  of graphical assets.
- To preserve that track record, we should prefer to bake / pre-render effects that might require complex processing  
  to render dynamically in Godot.
- After finalizing choice of font, we will convert the entire logo to a mesh to obtain a shared coordinate basis.




Do not yet make changes to the Python script. Instead, list any information that is needed but not provided here.   

