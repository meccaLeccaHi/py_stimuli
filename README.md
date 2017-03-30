# py_stimuli 

#### Python scripts for "game-like" packaging of neuroscience/psychophysics experiments. 

![alt text](http://i.imgur.com/9vY9tfZ.png "'Laser Morph' start-screen")

![alt text](https://i.ytimg.com/vi/4yBVK9NiLnI/hqdefault.jpg "'Laser Morph' screen grab")

[See video demo of *fixCont.py* on YouTube](https://youtu.be/Fa7tWZQfb8c)

**py_stimuli** is an iohub eye-tracking/joystick-compatible movie player.

Presentation of movies can be contingent on central fixation.
Currently, setup for an EyeLink(C) 1000 Desktop System. 
To use a different eye tracker implementation, change the iohub_tracker_class_path and eyetracker_config dict script variables.

Currently, loading raw (uncompressed) videos, future versions should read compressed movies-  
    video: H.264 compressed,  
    audio: Linear PCM  


These scripts make use of the following toolboxes:
## - Experiment software:
**Psychopy** http://www.psychopy.org/
- requires recent version that includes visual.MovieStim3() module, (which relies on MoviePy)

## - Eyetracking software:
**PyGaze** http://www.pygaze.org/

Proprietary tools:

**PyLink (for use of EyeLink eyetracker)** http://www.psychopy.org/api/hardware/pylink.html
## - Subject feedback (via gamepad)
**PyGame -** http://www.pygame.org/

**Xbox Controller -**  Depends on Xbox 360 controller support for Python (xbox.py - Steven Jacobs) https://github.com/FRC4564/Xbox

### Each folder contains a single experiment (composed of two files):   

#### - constants.py
- Defines constant variables for each experiment (e.g. display size).

#### - experiment.py
- Script for executing actual experiment.

### Relies heavily on the examples provided by the following books:
_Python for Experimental Psychologists_ by Edwin S. Dalmaijer  
_Making Games with Python & Pygame_ by Al Sweigart  

**Created by Dr Adam Jones  
Department of Neurosurgery,  
University of Iowa,  
Iowa City IA, USA** 
