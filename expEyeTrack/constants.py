# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:00:59 2016

@author: adam
"""

import os

# display type (either 'pygame' or 'psychopy')
DISPTYPE = 'psychopy'

# check os and assign directory
if os.name=='nt':
    from win32api import GetSystemMetrics
    # display resolution (should match monitor settings!)
    DISPSIZE = (int(GetSystemMetrics(0)/2),int(GetSystemMetrics(1)/2))

    HOMEDIR = 'C:/Users/adam/Desktop/virtBox_share/'
else:
    
    # display resolution (should match monitor settings!)
    DISPSIZE = (1920, 1080)

    HOMEDIR = '/home/adam/Desktop/virtBox_share/'
    # HOMEDIR = '/media/sf_vb_share/'

# directory where stimuli are located
STIMDIR = HOMEDIR + 'JonesStimset/'

#SCREEN = 1