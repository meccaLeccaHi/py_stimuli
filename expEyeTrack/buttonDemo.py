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

    img_pos_list = np.array([[0,height/8],[height/6,0],[0,-height/8],[-height/6,0]])
    movie_pos_list = np.array([[0,height/3.5],[height/3.5,0],[0,-height/3.5],[-height/3.5,0]])
    
    # Choose which button image to show    
    #button_image = "buttonIcon_N64.png"
    button_image = "xbox_dpad.png"
    cue_image = "xbox_dpad_cue.png"
    
    # Create list of functions corresponding to each button used
    cmd_list = [lambda:joystick.dpadUp(),
                lambda:joystick.dpadRight(),
                lambda:joystick.dpadDown(),
                lambda:joystick.dpadLeft()]  
    
#    cmd_list = [lambda:joystick.Y(),
#                lambda:joystick.B(),
#                lambda:joystick.A(),
#                lambda:joystick.X()]  
    
    RECORD = 0
    
    train_rep = 0
    
    vid_play = True
    
    repeat_demo = True
    
    while repeat_demo:
                          
        img = visual.ImageStim(win=win, image=button_image, units="pix")
        img.size *= .75  # scale the image relative to initial size
        
        cue_img = visual.ImageStim(win=win, image=cue_image, units="pix")
        cue_img.size *= .75  # scale the image relative to initial size
        
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
                                   
        press_text = visual.TextStim(win, text="PRESS",
                                   height=25,
                                   alignHoriz='center',
                                   bold=True,
                                   wrapWidth = width,
                                   color = 'yellow') 
                         
        # Show warning and animate fade
        if train_rep==0:
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
            
#            img.pos = img_pos_list[i]
#            cue_img.pos = img_pos_list[i]
            
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
                # Check joystick for button presses    
                if joystick.Start() or (' ' in keys):
                    mov.status = visual.FINISHED
                    vid_play = False
                    repeat_demo = False
                    break
            
            if vid_play==False:
                break
            
            ## Cue button press
                    
#            cue_img.draw()
#            mov.draw()
#            instr_text.draw()
#            fin_text.draw()
            press_text.pos = img_pos_list[i]
#            press_text.draw()
            
#            # Display updated stim on screen
#            win.flip()
#            if RECORD:
#                # store an image of every upcoming screen refresh:
#                win.getMovieFrame(buffer='back')
                
            press_text.contrast = 1  
        
            # Instruct user to press 'Start' and wait on button press
            while cmd_list[i]()==0:
            
                time.sleep(.05)
                
                # Oscillate text contrast while we wait
                if press_text.contrast:
                    press_text.contrast = 0
                else:
                    press_text.contrast = 1
                
                cue_img.draw()
                mov.draw()
                instr_text.draw()
                fin_text.draw()
                press_text.draw()    
                win.flip()
                if RECORD:
                    # Store an image of every upcoming screen refresh:
                    win.getMovieFrame(buffer='back')
                 
                if joystick.Start() or (' ' in keys):
                    vid_play = False
                    break
            
            # Iterate image orientation (rotation)
            img.ori += 90.0
            cue_img.ori += 90.0
            
            ## If trial break variable is set, break trial
            if vid_play==False:
                break
                
            # Current Trial is Done
            # Pause for 1 sec (while checking for button presses)    
            t_start = time.time()+1
            while time.time()<t_start:
                # Check keyboard for button presses
                keys = keyboard.getPresses()
                # Check joystick for button presses    
                if joystick.Start() or (' ' in keys):
                        vid_play = False
                        break
                    
        while vid_play:
            
            # Text to repeat or proceed
            loop_text = visual.TextStim(win, text="Repeat? <Back>\nProceed: <Start>",
                                   height=30,
                                   alignHoriz='center',
                                   wrapWidth = width) 
            loop_text.draw()    
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
                                   
            if joystick.Back():
                break
            elif joystick.Start():
                repeat_demo = False
                break
            
        train_rep += 1
        
        ## If trial break variable is set, break trial
        if vid_play==False:
            break
        
    ## End 
