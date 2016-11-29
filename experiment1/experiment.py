# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:42:29 2016

@author: adam
"""

import pygaze
from pygaze.display import Display
from pygaze.screen import Screen
import pygaze.libtime as timer
import numpy
from psychopy.visual import GratingStim

# Initialize a new Display instance (specifications are in
# constants.py).
disp = Display()

# Create a new GratingStim. The sinusoidal texture and the
# Gaussian mask will make it into a Gabor. The spatial
# frequency of 0.05 cycles per pixel will make it have
# 1 cycle every 20 pixels.
gabor = GratingStim(pygaze.expdisplay, tex='sin', mask='gauss', \
    sf=0.05, size=200)

# Initialize a new Screen instance for the Gabor.
gaborscreen = Screen()
# Add the GratingStim to the gaborscreen's screen property
# (a list of all PsychoPy stimuli in the screen).
gaborscreen.screen.append(gabor)

# Create random numbers between 0 and 1 (numpy.random.rand),
# converted to numbers between 0 and 2 (*2), and
# then converted to numbers between -1 and 1 (-1). The size
# must be a power of 2!
noise = (numpy.random.rand(64, 64) * 2) -1

# Create a new GratingStim. Using the noise array as
# texture will result in visual snow. The mask is Gaussian
# (to match the Gabor).
noisepatch = GratingStim(pygaze.expdisplay, tex=noise, \
    mask='gauss', size=200)
    
# Initialize a new Screen instance for the noise.
noisescreen = Screen()

# Add the GratingStim to the Screen's screen property (as
# with Gabor).
noisescreen.screen.append(noisepatch)

# Fill the Display with the Gabor Screen that ws prepared
# earlier.
disp.fill(gaborscreen)

# Present the Display (Gabor will now be on the monitor).
disp.show()

# Wait for 1000 milliseconds (Gabor is still on the
# monitor).
timer.pause(1000)

# Fill the Display with the noise Screen that ws prepared
# earlier.
disp.fill(noisescreen)

# Present the Display (noise is now on the monitor).
disp.show()

# Wait for 2000 milliseconds (noise is still on the monitor).
timer.pause(2000)

# Close the Display (this will end the experiment).
disp.close()