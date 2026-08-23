## nebula-notes.md

In Godot, the camera on the title screen scene will be fixed.

The background color will be black.

The nebula is not meant to be a full, solid cloud, but rather a distribution of 
clouds of different shapes and different levels of transparency.

It is preferable if the clouds of the nebula are able to slowly morph in shape and 
color, fading in and eventually fading back out.
Because of this preference for a slow, subtle animation, we will explore your suggestion 
to use two or three pre-rendered transparent layers on simple planes or 2D nodes.

The existing version of the game achieves its nebula effect by using this method.
The game does not have an animated nebula in its title screen. An animated nebula
on the title screen will be an enhancement over the existing version of the game. 
The existing game does create a slowly animated nebula during actual gameplay, using the
following method:
- It loads one base 2D image made from the GIMP 'plasma' effect that contains
  multiple colors, each color zone transitioning to the other via a gradient.
- Then, it loads several noise images, generated using Perlin noise with differing
  parameters.
- Finally, the noise images are stacked in front of the base color image, and their
  blend modes are adjusted so that the noise images behave like masks that hide or
  reveal the image behind them. For animation, all the images are rotated slowly,
  with each image rotating in the opposite direction from the one behind it.

The dominant colors of the static background in the current title screen tend to be green, 
ranging from light to dark green, and purple, ranging from deep purple to light red.

However, the colors of the animated nebula in the game range across the entire 
spectrum of visible light.

Some further guidance: the nebula effect should have
- dark overall exposure;
- diffuse clouds with occasional filaments that are also diffuse;
- no star field for now; we will add a starfield once we have a satisfactory nebula.

We are aiming for an overall character that resembles the early CGI space nebulas used 
in the 1990s show 'Babylon 5'. In that show, the background of space contains nebulas
that are mostly diffuse, but occasionally contain filaments. The filaments we create,
however, should also be diffuse and ephemeral in character.

Foreground object locations in the final frame:
- The desert moon and forest planet will sit in offset positions in the final frame,
  on either side of the logo.
- The moon will sit above and to the left of the logo.
- The logo itself will occupy center position.
- The planet will sit below and to the right of the logo.
- These positions are relative and we will iterate with exact positions until we
  reach our desired final placements.
  
If we determine that replicating the existing game's animated nebula is too expensive
in terms of file size and/or shader complexity in Godot, we will fall back to a static 
opaque 3840×2160 nebula rendered in Blender, with a 1200×675 preview and all procedural 
generation baked into the final PNG, as you suggested.

