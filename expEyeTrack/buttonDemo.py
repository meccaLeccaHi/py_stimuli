# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:49:07 2017

@author: root
"""

def buttonDemo( win, joystick, keyboard ):
    
    from psychopy import visual # core, 
#    from psychopy.iohub.client import launchHubServer
    
    # Force psychopy to use particular audio library
    from psychopy import prefs
    prefs.general['audioLib'] = ['pygame']
    from psychopy import sound
    
    import glob, gtk, time # , csv, datetime
    import numpy as np
    
    # Find movies matching wildcard search
    videopath = '/home/adam/Desktop/py_stimuli/JonesStimset/'
    videolist = glob.glob(videopath + '*rad_100_audVid.avi')
    videolist.sort()
    
     # Get current screen size (works for single monitor only)
    width = gtk.gdk.screen_width()
    height = gtk.gdk.screen_height()
    
    TESTING = 0
    
    RECORD = 0
    
    vid_play = True
    
    # Set screen parameters
    if TESTING:
        FLSCRN = False
        # Scale screen for testing
        SCREEN_SIZE = np.array([(x/1.5) for x in (width, height)])
        # We're referencing pixels, so must be in integer values
        SCREEN_SIZE = np.floor(SCREEN_SIZE)
    else:
        FLSCRN = True
        SCREEN_SIZE = np.array([width, height])
                        
    img = visual.ImageStim(win=win, image="buttonIcon_N64.png",
                                        units="pix")
    img.size *= 1.25  # scale the image relative to initial size
    
    instr_text = visual.TextStim(win, text="Identify each with these buttons:",
                               height=30,
                               alignHoriz='center',
                               wrapWidth = width,
                               pos = [0, height/2 - 50]) 
                               
    fin_text = visual.TextStim(win, text="<Press Start to skip>",
                               height=35,
                               alignHoriz='center',
                               italic=True,
                               wrapWidth = width,
                               color = 'grey',
                               pos = [0, -height/2 + 50]) 
    
    img_pos_list = np.array([[0,height/10],[height/10,0],[0,-height/10],[-height/10,0]])
    movie_pos_list = np.array([[0,height/3.5],[height/3.5,0],[0,-height/3.5],[-height/3.5,0]])
                         
    # Show count-down        
    text = visual.TextStim(win,height=48,
                               text="Remember these people...",
                               alignHoriz='center')

    # Animate
    text.contrast = 1
    for i in np.array(range(100,-100,-2))/100.0:
        text.contrast = i 
        text.draw()    
        win.flip()
        if RECORD:
            # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
            
    for i in range(len(videolist)):
        
        img.pos = img_pos_list[i] 
        
        # Draw the image to window and show on screen
        img.draw()
        instr_text.draw()
        fin_text.draw()
        win.flip()
        
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win, videolist[i]) 
        mov.size *= .75  # scale the image relative to initial size
        mov.pos = movie_pos_list[i]
        
        # Start the movie stim by preparing it to play
        mov.play()
        
        # If boolean to finish current movie AND movie has not finished yet
        while mov.status != visual.FINISHED:
            
            # Draw movie stim again
            mov.draw()
            img.draw()
            instr_text.draw()
            fin_text.draw()
    
            # Display updated stim on screen
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
            
            # Check keyboard for button presses
            keys = keyboard.getPresses()
        
            # Check any new keyboard char events for a space key
            # If one is found, set the trial end variable
            if ' ' in keys:
                mov.status = visual.FINISHED
                
            # Check keyboard for button presses
            keys = keyboard.getPresses()
            # Check joystick for button presses    
            if joystick.Start() or (' ' in keys):
                    vid_play = False
                    break
                
        # Iterate image orientation (rotation)
        img.ori += 90.0
        
        ## If trial break variable is set, break trial
        if vid_play==False:
            break
            
        # Current Trial is Done
            
        t_start = time.time()+1
        while time.time()<t_start:
            # Check keyboard for button presses
            keys = keyboard.getPresses()
            # Check joystick for button presses    
            if joystick.Start() or (' ' in keys):
                    vid_play = False
                    break
        
    ## End 
