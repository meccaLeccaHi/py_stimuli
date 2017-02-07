# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:22:30 2017

@author: root
"""

from psychopy.hardware import joystick
from psychopy import visual
import pygaze.libtime as timer


# input
joy = joystick.Joystick(0)

# # # # #
# RUN

# run until a minute has passed
t0 = timer.get_time()
t1 = timer.get_time()
text = "Test the joystick!"
while t1 - t0 < 10000:
    
    print joy.getAllButtons()
    print joy.getAllHats()
    
    t1 = timer.get_time()
    
#    win.flip()  # flipping implicitly updates the joystick info
     
#    if event=="joybuttonpress" and value==3:
#        print "button pressed"
#        print t1
#        break

# # # # #
# CLOSE





