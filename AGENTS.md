This project aims to create a new logo and two other assets for the title
screen of a video game: a 3D model of a planet, a 3D model of a moon, and a 
colorful nebula background.

This file contains conventions for working on this project.

Python scripts are the source of truth for this project.  
.blend files are to be regarded as generated artifacts.  

A preview image in png format should be created each time a  
new .blend file is generated.  

Scripts should be placed in the scripts/ directory.
.blend files should be placed in the blendfiles/ directory.
Preview images should be placed in the renders/ directory.

Python script names for the logo should follow the form "logo-XXX-YYY.py" where XXX  
is a version number and YYY is an experiment number within the version.  

Python script names for the planet should follow the form "planet-XXX-YYY.py" where XXX  
is a version number and YYY is an experiment number within the version.  

Python script names for the moon should follow the form "moon-XXX-YYY.py" where XXX  
is a version number and YYY is an experiment number within the version.  

Python script names for the nebula should follow the form "nebula-XXX-YYY.py" where XXX  
is a version number and YYY is an experiment number within the version.  

.blend file names for the logo should follow the form "logo-XXX-YYY.blend", matching  
the version number and experiment number of the script.

.blend file names for the planet should follow the form "planet-XXX-YYY.blend", matching  
the version number and experiment number of the script.

.blend file names for the moon should follow the form "moon-XXX-YYY.blend", matching  
the version number and experiment number of the script.

.blend file names for the nebula should follow the form "nebula-XXX-YYY.blend", matching  
the version number and experiment number of the script.

Preview files for the logo should follow the form "logo-XXX-YYY.png" to mirror the  
version and experiment number of the current script and .blend file.

Preview files for the planet should follow the form "planet-XXX-YYY.png" to mirror the  
version and experiment number of the current script and .blend file.

Preview files for the moon should follow the form "moon-XXX-YYY.png" to mirror the  
version and experiment number of the current script and .blend file.

Preview files for the nebula should follow the form "nebula-XXX-YYY.png" to mirror the  
version and experiment number of the current script and .blend file.

Version and experiment numbers are tracked independently for the logo, planet, moon, and nebula.

An experiment number is consumed only when Blender successfully generates the required .blend  
file and preview image. A failed invocation may be corrected and rerun under the same experiment number.

Start version numbers with 001 and increment by 1 only when instructed to start a new version.  

Start experiment numbers with 001 and increment by 1 after each successful run that generates the required .blend file and preview image.

When instructed to start a new script version, reset the experiment number to 001.

Python scripts prior to the current version number and experiment number should be treated  
as historical and not overwritten.  

.blend files and preview files prior to the current version number and  
experiment number should be treated as historical and not overwritten.

A Python script version number is meant to track a design iteration.  
An experiment number is meant to track an adjustment within a design iteration. 
Each experiment number has a 1:1 relationship with a successful artifact-generating Blender run.

After each successful artifact-generating Blender run, create a file of notes and observations  
in markdown form, and place it in the notes/ directory.
Notes for the logo should be saved with the filename form "notes-XXX-YYY.md".
Notes for the planet should be saved with the filename form "planet-XXX-YYY.md".
Notes for the moon should be saved with the filename form "moon-XXX-YYY.md".
Notes for the nebula should be saved with the filename form "nebula-XXX-YYY.md".

A notes file should contain:
- an interpretation of the instructions given for that run  
- observations on whether the latest preview image fulfills the aim of the current  
  design iteration  
- a comparison of the latest preview image with the previous preview image, if it exists,
  including cases where the previous preview is the final preview of the preceding version

Note files from prior runs are to be treated as historical and not overwritten.
This convention is meant to capture a history of decisions as the overall design 
of the asset evolves.

If a prompt is unclear, do not make any file modifications or invoke blender,  
but instead report on the part that lacks clarity and stop.  

If a prompt contradicts the conventions given in this file, do not  
make any file modifications or invoke blender, but instead report the  
contradiction and stop.

A local git repository has been created, and will be updated with commits on each  
successful run of blender. Feel free to use the git repository for reference  
while working on the current run, but do not make any commits.

If you find that the repository is not in the state that you are told, do not make  
any file modifications or invoke blender, but instead report on the inconsistency  
and stop.

The fonts/ directory contains a number of Google fonts that have been chosen as  
candidates for use on the logo. If a font other than the one in use seems better  
suited to the current design objective, recommend changing to that font in your  
notes for that run. Do not begin using a different font without approval.

The exports/ directory has been added for saving .glb files. We will save a .glb file  
when we are ready to test a 3D object in Godot. If this workflow works well, we may create  
and export other objects for use in the title screen.

Name export files for the logo in the form 'logo-XXX-YYY.glb' using the version number 
and experiment number.

Name export files for the planet in the form 'planet-XXX-YYY.glb' using the version number 
and experiment number.

Name export files for the moon in the form 'moon-XXX-YYY.glb' using the version number 
and experiment number.

Name export files for the nebula in the form 'nebula-XXX-YYY.glb' using the version number 
and experiment number.


Prior GLB exports are historical and should not be overwritten.

A textures/ directory exists now for saving and loading textures.  
The textures/ directory may also contain reference textures placed there by the developer.
For files generated by Codex, here are the guidelines for naming:
- Placeholder values:
  {map}: basecolor, orm, normal, emission, or height
  {resolution}: 8k, 4k, 2k, 1k, or 512
- Generated textures for the logo should be saved using the file name convention "logo-XXX-YYY-{map}-{resolution}.png".
- Generated textures for the planet should be saved using the file name convention "planet-XXX-YYY-{map}-{resolution}.png".
- Generated textures for the moon should be saved using the file name convention "moon-XXX-YYY-{map}-{resolution}.png".
- Generated textures for the nebula should be saved using the file name convention "nebula-XXX-YYY-{map}-{resolution}.png".


  Examples:
  logo-003-001-basecolor-2k.png
  logo-003-001-orm-2k.png
  logo-003-001-orm-1k.png
  logo-003-001-normal-512.png
  logo-003-001-emission-1k.png
  logo-003-001-height-2k.png

  planet-003-001-basecolor-2k.png
  planet-003-001-orm-2k.png
  planet-003-001-orm-1k.png
  planet-003-001-normal-512.png
  planet-003-001-emission-1k.png
  planet-003-001-height-2k.png

  moon-003-001-basecolor-2k.png
  moon-003-001-orm-2k.png
  moon-003-001-orm-1k.png
  moon-003-001-normal-512.png
  moon-003-001-emission-1k.png
  moon-003-001-height-2k.png
  
For the nebula, we will use a filename convention with identifiers such as:
- background
- cloud01
- cloud02
- cloud03
- composite

Example filenames:
- nebula-001-001-background-4k.png
- nebula-001-001-cloud01-2k.png
- nebula-001-001-cloud02-2k.png
- nebula-001-001-cloud03-2k.png
- nebula-001-001-composite-4k.png

Generated production images of the nebula belong in textures/, while the mandatory 
1200×675 experiment preview still remains in renders/.

Treat existing texture files as historical and do not overwrite them.

