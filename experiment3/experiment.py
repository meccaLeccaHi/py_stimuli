# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:01:03 2016

@author: adam
"""

from constants import DISPSIZE
import random
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.sound import Sound

# create a new Display instance (to interact with the
# monitor)
disp = Display()

# create a new Screen (to use as a canvas to draw on)
scr = Screen()

# Create two Sounds, one for nice and one for stern
# feedback
sine = Sound(osc='sine', freq=4000, length=500)
noise = Sound(osc='whitenoise', length=500)

# a list of vowels
vowels = ['a', 'e', 'i', 'o', 'u', 'y']

# create a new Keyboard instance, to monitor key presses
kb = Keyboard(keylist=vowels, timeout=None)

# randomly choose one vowel
letter = random.choice(vowels)

# draw the vowel on a Screen
scr.draw_text(text=letter, fontsize=128)

# fill the Display with a Screen and update the monitor
disp.fill(scr)
disp.show()

# wait for a response
key, presstime = kb.get_key()

# check if the pressed key matches the displayed letter
if key == letter:
    correct = 1
else:
    correct = 0
    
# on a correct response
if correct:
    #...provide nice feedback
    feedback = "Well done!"

    # (0,255,0) is green
    fbcolor = (0, 255, 0)
# on an incorrect response...
else:

    #...provide nasty feedback
    feedback = "You're wrong!"

    # (255,0,0) is red
    fbcolor = (255, 0, 0)
    
# construct an informative string by using variables
extrafb = 'The vowel was %s, and you typed %s.' \
    % (letter, key)
    
# first clear the Screen of its current content
scr.clear()

# then draw the feedback text
scr.draw_text(text=feedback, colour=fbcolor, fontsize=24)

# determine the position of the extra feedback

# (at half the screen width, and 60% of the screen height)
extrafbpos = (int(DISPSIZE[0]*0.5), int(DISPSIZE[1]*0.6))

# draw the extra feedback
scr.draw_text(text=extrafb, pos=extrafbpos, fontsize=24)

# show the Screen with feedback
disp.fill(scr)
disp.show()

# on a correct response...
if correct:
    
    #...play the sine Sound
    sine.play()
    # on an incorrect response...
else:
    #...play the harsh Sound
    noise.play()
    
# wait for any keypress
kb.get_key(keylist=None, timeout=None)

# close the Display
disp.close()