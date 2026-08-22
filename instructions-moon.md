# instructions-moon.md  

This file contains artistic instructions for building the moon for the game title screen.  

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

The game that this asset is being designed for is a mobile game that initially existed on iPhone, and was  
originally released in 2012. Originally, it ran on the Cocos2d-ObjectiveC game engine, and is now being  
rebuilt on Godot version 4, with plans to re-release for iOS, and also release for Android.  

This is a 2D space game that features gravity as a central game dynamic. The artistic feel for the game  
is retro sci-fi, with artistic inspiration from films such as Forbidden Planet and War of the Worlds.  

### About the moon  

The existing moon in the title screen is a desert moon, large enough to qualify as a dwarf planet.

The moon can be made from creating a sphere mesh and applying the "desert-moon.png" texture  
found in the textures/ directory. There is also a subfolder there that contains images for height,  
normal, orm, and roughness, all in png format.
The named desert-moon and forest-planet files are reusable authored source textures and are not  
governed by the generated experiment-texture naming convention.

Preview files should be generated at 1200×675 resolution.
Use the Eevee rendering engine.

### Current Design Phase: Create the desert moon in 3D space  

- Here is our sequence of steps for creating the moon:
  - Create one sphere mesh with a radius of 3 Blender units.
  - Apply the textures/desert-moon.png texture to the sphere mesh.
  - Maps for height, normal, orm, and roughness:
    - textures/desert-moon/desert-moon_height.png
    - textures/desert-moon/desert-moon_normal.png
    - textures/desert-moon/desert-moon_orm.png
    - textures/desert-moon/desert-moon_roughness.png
- Some guidance for using these files:
  - Use roughness from the ORM map’s green channel; retain the separate roughness image only as a source/reference file.
  - Use the height map for bump shading only.
  - Treat the normal map as tangent-space OpenGL/Y+.
  - base-color image (textures/desert-moon.png): Principled BSDF Base Color, sRGB.
  - ORM: separate RGB channels, Non-Color.
  - normal: Normal Map node, Non-Color.
  - height: bump shading only, no mesh displacement, Non-Color.
- Use a standard equirectangular UV sphere. 
- Put the longitudinal seam on the rear side and orient the most visually interesting region 
  toward the camera.
- Use a perspective camera, and start with Blender's default focal length of 50mm.
- We can iterate through focal length adjustments as needed.
- For now, place the camera to create a centered composition.
- The moon should occupy roughly 1/4 of the frame height.
- Use a black background color.
- Where possible, choose a UV-sphere resolution substantially below 25,000 triangles while maintaining a smooth rendered silhouette.
- The base-color photographs contain baked tonal variation, and this is acceptable.
- Feed the normal texture through a Normal Map node into the Normal input of a Bump node. 
- Feed the height texture into that Bump node’s Height input, then connect the Bump node output to the Principled BSDF Normal input.
- Begin with Normal Map strength 1.0, Bump strength 0.15, and Bump distance 0.1 Blender units. Adjust these values through later experiments.


- We are going to introduce a three-light arrangement whose purpose is to improve edge definition and reveal the existing geometry. 
  Lighting should remain soft and should not create harsh shadows or strong specular hotspots.
  - First light
    - Name: Key Light
    - Type: Area light
    - Position: above, right, and slightly in front of the camera
    - Intensity: 1000 watts
    - Size: 1.5 m
  - Second light 
    - Name: Fill Light
    - Type: Area light
    - Position: Slightly above the camera
    - Intensity: 600 watts
    - Size: 1.5 m
  - Third light
    - Name: Rim Light
    - Type: Area light
    - Position: Behind the moon, above and center
    - Intensity: 400 watts
    - Size: 1.5 m
    

- Details needed for creating the moon preserved here:
  - Texture Policy
    - Author textures:
      - PNG
      - lossless
      - bit depth: 
        - 8-bit PNG for base color, ORM, emission, and normal
        - 16-bit grayscale PNG for height when displacement precision matters
        - 8-bit grayscale PNG for height when using only as bump shading guide
      - PBR compatible

    - Packing:
      - ORM: Red = Ambient Occlusion, Green = Roughness, Blue = Metallic
      
    - Shader Use:
      - Green should connect to Principled BSDF Roughness.
      - Blue should connect to Principled BSDF Metallic.
      - Do not apply the red ambient-occlusion channel in the initial Blender material;
        retain it for Godot/export testing.

    - Color Space:
      - Base Color: sRGB
      - Emission: sRGB
      - ORM: Linear
      - Normal: Linear
      - Height: Linear

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
      - Height: For the current 8-bit height map, use bump shading only. If a 16-bit displacement  
        source is authored later, retain that source and avoid downscaling it unless required.  
      - Avoid expensive runtime shaders unless an artistic benefit clearly justifies them.  

    - Triangle budget: 
      - Use a provisional scene-wide budget of 200,000–500,000 visible triangles, with the final hard ceiling  
        determined through testing on the oldest supported device tier.
      - Increase sphere resolution as needed for a smooth silhouette, but do not exceed 25,000 triangles without first requesting approval.

- To Be Decided:
  - A final moon-specific triangle target after sphere tessellation and surface-detail requirements are known.
  - Identify the oldest supported device or performance tier for validation, prior to final export.


