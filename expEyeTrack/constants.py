# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:00:59 2016

@author: adam
"""

import numpy,wx

## Set up display
# Display type (either 'pygame' or 'psychopy')
DISPTYPE = 'psychopy'

# Get current screen size (works for single monitor only)
app = wx.App(False)
DISPSIZE = wx.GetDisplaySize()

## Set paths
# Main directory
MAINDIR='/home/adam/Desktop/py_stimuli/'
# Directory where stimuli are located
STIMDIR=MAINDIR+'JonesStimset/'
# Directory where experiment is located
EXPDIR=MAINDIR+'expEyeTrack/'
# Directory where sounds are located
SNDDIR=EXPDIR+'sounds/'
# Directory where sounds are located
IMGDIR=EXPDIR+'images/'
# Directory where headers are located
HDRDIR=EXPDIR+'headers/'
# Define path for figure output
FIGDIR=EXPDIR+'beh_figs/'    

# Lateral side of controller to use
SIDE='L'
# Number of trials of each stimulus to run
BLOCK_REPS=1
# Decision cue window (seconds)
DEC_WIN=2
# Inter-stimulus interval (seconds)
ISI=1
# Jitter range (+/-seconds)
JITTER=.1
# Scaling of image (none = 1)
SCALE=1
# Volume of sound effects
SND_VOL=.25

# Boolean for debugging mode
TESTING=1; # 1: yes, 0: no
# Boolean for including control stimuli
CONTROLS=0; # 1: yes, 0: no
# Boolean for presence of tracker
EYE_TRACKER=0; # 1: yes, 0: no
# Boolean to simulate tracker activity with mouse
SIM_TRACKER=1; # 1: yes, 0: no
# Boolean for presence of joystick (N64 only, currently)
JOYSTICK=0; # 1: yes, 0: no1
# Boolean for intro music
MUSIC=1; # 1: yes, 0: no

# Define fades
FADEIN = tuple(numpy.array(range(-100,100,2))/100.0)
FADEOUT = tuple(numpy.array(range(100,-100,-2))/100.0)