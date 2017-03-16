# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:36:28 2017

@author: root
"""

import time
import psychopy.event as event

## Get devices for future access
#keyboard = io.devices.keyboard

cmd_list = [lambda:('up' in event.getKeys()),
            lambda:('right' in event.getKeys()),
            lambda:('down' in event.getKeys()),
            lambda:('left' in event.getKeys())] 

curr_time = time.time()

delay = 5

while time.time()-curr_time < delay:
    print(cmd_list[0]())
