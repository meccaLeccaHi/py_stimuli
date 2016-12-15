#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Loop of MovieStim
Different systems have different sets of codecs.
avbin (which PsychoPy uses to load movies) seems not to load compressed audio on all systems.
To create a movie that will play on all systems I would recommend using the format:
    video: H.264 compressed,
    audio: Linear PCM
"""

from __future__ import division

from psychopy import visual, core, event

#from pygaze.eyetracker import EyeTracker

import time, glob, pylinkwrapper

#tracker = EyeTracker(win , trackertype='eyelink')  # 'dumbdummy'
#tracker.calibrate()

win = visual.Window((1280, 1024),screen=0,color=[-1,-1,-1]) # 800, 600

#tracker = pylinkwrapper.Connect(win, '1_test')

#tracker.calibrate()

videopath = glob.glob('/home/adam/Desktop/virtBox_share/JonesStimset/identity1/*100_audVid.avi')

for vidPath in videopath:
    
    mov = visual.MovieStim3(win, vidPath, size=(366, 332),fps=30,
                            flipVert=False, flipHoriz=False, loop=False) # 320, 240
    print('orig movie size=%s' % mov.size)
    print('duration=%.2fs' % mov.duration)
    
#    tracker.set_trialid()
    
    fixation = visual.GratingStim(win, tex=None, mask='circle', sf=0, size=0.03,
                              name='fixation', autoLog=False)
                              
    photodiode = visual.GratingStim(win, tex=None, mask='none', sf=0, size=0.2,
                              name='photodiode', autoLog=False, pos=(1,-1))
    globalClock = core.Clock()

    while mov.status != visual.FINISHED:
        mov.draw()
        fixation.draw()
        photodiode.draw()
        win.flip()
        fixation.draw()
        if event.getKeys():
            break
        
    win.flip(clearBuffer=True)
    time.sleep(1)

#tracker.end_experiment('/home/adam/Desktop/')

win.close()
core.quit()

# The contents of this file are in the public domain.