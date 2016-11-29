# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:01:03 2016

@author: adam
"""

from constants import DISPSIZE
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard

# create a Display to show things on the monitor
disp = Display()

# create a Screen for drawing operations
scr = Screen()

# create a Keyboard to collect keypresses
kb = Keyboard(keylist=None, timeout=None)

# randomly choose one vowel
letter = random.choice(vowels)

# define a super-important question
question = 'What do you think of this question?'

 # define the question's position
qpos = (int(DISPSIZE[0]*0.5), int(DISPSIZE[1]*0.2))

# draw it on the Screen
scr.draw_text(text=question, pos=qpos, fontsize=24)

# fill the Display with the Screen
disp.fill(scr)

# present the current Display
disp.show()

# start with an empty response string
response = ''

# start undone
done = False

# loop until done == False
while not done:
    # check for keypresses
    key, presstime = kb.get_key()
    
    # check if the length of the key's name equals 1
    if len(key) == 1:
        
        # add the key to the response
        response += key
        
    # check if the key is the Space bar
    elif key == 'space':
        
        # add a space to the response
        response += ' '
        
    # check if the key's name was 'backspace' and
    # check if the response has at least 1 character
    elif key == 'backspace' and len(response) > 0:
    
        # remove the last character of the response
        response = response[0:-1]
        
    # if the key was none of the above, check if it
    # was the Enter key
    if key == 'return':
        
        # set done to True
        done = True
        
    # clear the current content of scr
    scr.clear()
    
    # redraw the question
    scr.draw_text(text=question, pos=qpos, fontsize=24)
    
    # draw the current response on a Screen
    scr.draw_text(text=response, fontsize=24)
    
    # fill the Display with the response Screen
    disp.fill(scr)
    
    # show the Display on the monitor
    disp.show()
    
# close the Display
disp.close()