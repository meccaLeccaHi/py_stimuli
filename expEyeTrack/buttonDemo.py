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

    # Choose which button image to show    
    #button_image = "buttonIcon_N64.png"
    button_image = "xbox_dpad.png"
    
    cmd_list = [lambda:joy.dpadUp(),
                lambda:joy.dpadRight(),
                lambda:joy.dpadDown(),
                lambda:joy.dpadLeft()]  
    
#    cmd_list = [lambda:joy.Y(),
#                lambda:joy.B(),
#                lambda:joy.A(),
#                lambda:joy.X()]  

#    cmd_list = [lambda: a(x,y), lambda: b(),...]  
#    for cmd in cmd_list:  
#        if cmd():  
#            break  
    
    RECORD = 0
    
    vid_play = True
                          
    img = visual.ImageStim(win=win, image=button_image,
                                        units="pix")
    img.size *= .5  # scale the image relative to initial size
    
    warn_img = visual.ImageStim(win=win, image="training_mode.png",
                                        units="pix")
    warn_img.size *= .75  # scale the image relative to initial size
                                       
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
                     
    # Show warning and animate fade
    warn_img.contrast = 1
    for i in np.array(range(100,-100,-1))/100.0:
#        warn_img.contrast = i 
        warn_img.draw()    
        win.flip()
        if RECORD:
            # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
                
    # Show instructions        
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
                
        # Cue button press
                
        # Wait on button press
        
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
