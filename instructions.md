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

### Current Design Phase: Review Python script  

Now that we have a good reproduction of the overall shape of the logo, this is a good moment to check on some  
details in our code.  

The game itself is a 2D game, but much of its artwork was created first in a 3D modeling/animation program similar  
to Blender, and then rendered out into animation frames.  

In addition, the title screen where this logo will appear was originally created in Photoshop, but employs a  
number of techniques to give depth to the scene.  

One desirable objective in this logo remake is to create a logo that is a 3D object that can be saved in glTF 2.0  
format, loaded into Godot, where the game is being rebuilt, and used there to create some subtle effects that  
give more life to the title screen than a static image.

Examine the Python script and identify all parts of the code that might be configured to use exclusively 2D    
capability. Report the current state of the code, and list all the changes that may need to be made in order  
to create the logo as a 3D object and save it in glTF 2.0 format, specifically as a GLB file.

Do not make any changes to the code yet, and do not invoke Blender. We will increment the version number  
and reset the experiment number on the next set of files we create, but at the moment, we are conducting  
a read-only review.


