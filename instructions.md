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

The shape of the logo follows a gentle arc from left to right, as if it sat on the upper left quarter of  
a circle. 

### Current Design Phase: Lighting and refining shape  

- The text of the logo is "PLANETBUILDER", all in uppercase.
- We will continue using the Days One font.  

- For the sake of experimentation, let's assume the arc that forms the baseline of the logo  
  has a radius of 10 Blender units.
- Character size and spacing should remain approximately established, allowing the word to cover
  more than 90 degrees or wrap around the circle.
- Each character should rotate around Z to follow the local tangent of the circular baseline.
- Placement on the arc should happen after the shared X=20 degrees and Y=20 degrees rotations.


- Here is our sequence of steps for creating and shaping the logo:
  - Create one 3D text object for each character, positioning them to preserve the Days One font’s original character advances and kerning.
  - Convert each character’s text object into a separate mesh.
  - Rotate all character meshes together as a group positive 20 degrees around the X axis, using a shared pivot.
  - Rotate the entire group of meshes positive 20 degrees around the Y axis, so the left side advances toward the camera while the right side recedes.
     
- Let's modify the default material being used for the character meshes.
  - Our primary change is going to be a color gradient that spans the entire logo,
    moving from left to right in color and roughness.
  - We will transition (left to right) across four colors: red, orange, yellow, and cream.
  - Values for material roughness:
    - Red will have roughness of 0.3
    - Orange will have roughness of 0.25
    - Yellow will have roughness of 0.2
    - Cream will have roughness of 0.1
  - Spread the transition evenly (each color and roughness level getting about 25 percent of the logo)
  - Keep highlights soft so as to avoid hot spots.
  - Allow bevels to catch light.

- We are going to introduce a three-light arrangement whose purpose is to improve edge definition and reveal the existing geometry. 
  Lighting should remain soft and should not create harsh shadows or strong specular hotspots.
  - First light
    - Name: Key Light
    - Type: Area light
    - Position: above, right, and slightly in front of the camera
    - Intensity: 1.0
    - Size: Large
  - Second light (this replaces the existing light we have been using)
    - Name: Fill Light
    - Type: Area light
    - Position: Slightly above the camera
    - Intensity: 0.3
    - Size: Large
  - Third light
    - Name: Rim Light
    - Type: Area light
    - Position: Behind the logo, above and toward the left side
    - Intensity: 0.5
    - Size: Large
    
- Bring the camera 10 percent closer on the Z axis.
- Move the key light and fill light so that they keep their relative position to the camera.


- Details needed for creating logo preserved here:
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


