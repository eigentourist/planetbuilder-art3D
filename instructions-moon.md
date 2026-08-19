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

The moon can reliably be made from creating a sphere mesh and applying the "desert-moon.png" texture  
found in the textures/ directory.

### Current Design Phase: Explore relative positions in 3D space  


- Here is our sequence of steps for creating the moon:
  - Create one sphere mesh with a radius of 3 Blender units.
  - Apply the textures/desert-moon.png texture to the sphere mesh.
     

- We are going to introduce a three-light arrangement whose purpose is to improve edge definition and reveal the existing geometry. 
  Lighting should remain soft and should not create harsh shadows or strong specular hotspots.
  - First light
    - Name: Key Light
    - Type: Area light
    - Position: above, right, and slightly in front of the camera
    - Intensity: 1.0
    - Size: Large
  - Second light 
    - Name: Fill Light
    - Type: Area light
    - Position: Slightly above the camera
    - Intensity: 0.3
    - Size: Large
  - Third light
    - Name: Rim Light
    - Type: Area light
    - Position: Behind the moon, above and center
    - Intensity: 0.5
    - Size: Large
    

- Details needed for creating the moon preserved here:
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
      - One atlas.
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
      - Use an initial limit of 25,000 triangles for the moon, with a preference for substantially fewer  
        whenever the silhouette remains visually smooth.

- To Be Decided:
  - A final moon-specific triangle target after lettering and bevel complexity are known.
  - Identify the oldest supported device or performance tier for validation, prior to final export.


