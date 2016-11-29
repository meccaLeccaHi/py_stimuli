# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:29:48 2016

@author: adam
"""

from pygaze.display import Display
from pygaze.screen import Screen
import pygaze.libtime as timer

# disp = Window(size=DISPSIZE, units='pix', fullscr=True)
disp = Display()
fixscreen = Screen()
fixscreen.draw_fixation(fixtype='dot')

imgscreen = Screen()
imgscreen.draw_image('/home/adam/Desktop/experiment0/Example.png')

disp.fill(fixscreen)
disp.show()
timer.pause(1000)

disp.fill(imgscreen)
disp.show()
timer.pause(2000)

disp.close()