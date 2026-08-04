This project aims to create a new logo for a video game.  
This file contains conventions for working on this project.

Python scripts are the source of truth for this project.  
.blend files are to be regarded as generated artifacts.  

A preview image in png format should be created each time a  
new .blend file is generated.  

Scripts should be placed in the scripts/ directory.
.blend files should be placed in the blendfiles/ directory.
Preview images should be placed in the renders/ directory.

Python script names should follow the form "logo-XXX-YYY.py" where XXX  
is a version number and YYY is an experiment number within the version.  

.blend file names should follow the form "logo-XXX-YYY.blend", matching  
the version number and experiment number of the script.

Preview files should follow the form "logo-XXX-YYY.png" to mirror the  
version and experiment number of the current script and .blend file.

Start version numbers with 001 and increment by 1 only when instructed to start a new version.  

Start experiment numbers with 001 and increment by 1 on each run.

When instructed to start a new script version, reset the experiment number to 001.

Python scripts prior to the current version number and experiment number should be treated  
as historical and not overwritten.  

.blend files and preview files prior to the current version number and  
experiment number should be treated as historical and not overwritten.

A Python script version number is meant to track a design iteration.  
An experiment number is meant to track an adjustment within a design iteration,  
and has a 1:1 relationship with each run of blender.

After each run of blender, create a file of notes and observations in markdown form,  
and place it in the notes/ directory, with the filename form "notes-XXX-YYY.md".

A notes file should contain:
- an interpretation of the instructions given for that run  
- observations on whether the latest preview image fulfills the aim of the current  
  design iteration  
- a comparison of the latest preview image with the previous preview image, if it exists,
  including cases where the previous preview is the final preview of the preceding version

Note files from prior runs are to be treated as historical and not overwritten.
This convention is meant to capture a history of decisions as the overall logo design evolves.

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

Name export files in the form 'logo-XXX-YYY.glb' using the version number and experiment number.  
Prior GLB exports are historical and should not be overwritten.

A textures/ directory exists now for saving textures. Textures should be placed in this directory,  
using the file name convention "logo-XXX-YYY-{map}-{resolution}.png".
  Placeholder values:
  {map}: basecolor, orm, normal, emission, or height
  {resolution}: 2k, 1k, or 512


  Examples:
  logo-003-001-basecolor-2k.png
  logo-003-001-orm-2k.png
  logo-003-001-orm-1k.png
  logo-003-001-normal-512.png
  logo-003-001-emission-1k.png
  logo-003-001-height-2k.png

Treat existing texture files as historical and do not overwrite them.

