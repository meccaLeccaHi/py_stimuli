# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:49:07 2017

@author: root
"""

def buttonDemo( win, joy, keyboard, cmd_list, side='L' ):
    
    from psychopy import visual # core, 
#    from psychopy.iohub.client import launchHubServer
    
    # Force psychopy to use particular audio library
    from psychopy import prefs
    prefs.general['audioLib'] = ['pygame']
    from psychopy import sound
    
    import glob, wx, time, os # , csv, datetime
    import numpy as np
    
    # Volume of sound effects
    SND_VOL=.25
    
    def laserSound():
        # Acknowledge button press with sound
        filesound = sound.Sound(value = "laser.wav")
        filesound.setVolume(SND_VOL*2)
        filesound.play()

    # Find movies matching wildcard search
    videopath = os.environ['HOME']+"/Desktop/py_stimuli/JonesStimset/"
    videolist = glob.glob(videopath + '*rad_100_audVid.avi')
    videolist.sort()
    
     # Get current screen size (works for single monitor only)
    app = wx.App(False)
    width, height = wx.GetDisplaySize()

    img_pos_list = np.array([[0,height/7],[height/6,0],[0,-height/7],[-height/6,0]])
    movie_pos_list = np.array([[0,height/3.5],[height/3.5,0],[0,-height/3.5],[-height/3.5,0]])
    
    # Choose which button image to show    
    #button_image = "buttonIcon_N64.png"
    button_image = "xbox_dpad.png"
    cue_image = "xbox_dpad_cue.png"
       
    if side=='R':
        img_list_button = ["xbox_Y.png","xbox_B.png","xbox_A.png","xbox_X.png"]
        img_list_cue = img_list_button
#        
#        # Create list of functions corresponding to each button used
#        cmd_list = (lambda:joy.Y(),
#                    lambda:joy.B(),
#                    lambda:joy.A(),
#                    lambda:joy.X())
    else:
        img_list_button = [button_image]*4
        img_list_cue = [cue_image]*4
#        
#        # Create list of functions corresponding to each button used
#        cmd_list = (lambda:joy.dpadUp(),
#                    lambda:joy.dpadRight(),
#                    lambda:joy.dpadDown(),
#                    lambda:joy.dpadLeft()) 
        
    wait_img_list = ["xbox_start.png", "xbox_back.png"] 
        
    train_rep = 0
    
    vid_play = True
    
    repeat_demo = True
    
    # Load images
    warn_img = visual.ImageStim(win=win, image="training_mode.png",units="pix")
    dec_img = visual.ImageStim(win=win,image="decision.png",units="pix")
    dec_hl_img = visual.ImageStim(win=win,image="decision_hl.png",units="pix")
    
    # Create vector of log-distributed values for fade effect                           
    NewRange = (1.0 - -1.0)  
    logDist = (np.logspace(0, 1.0, 100, endpoint=True) / 10)
    scaled_logDist = tuple(((logDist * NewRange) + -1.0)*-1)
        
    while repeat_demo:
        
        # Reset contrast of decision images                                 
        dec_img.contrast = 1
        dec_hl_img.contrast = 1
        
        # Create text objects          
        instr_text = visual.TextStim(win, text="...by pressing these buttons:",
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
                                   pos=[0,-height/2 + 50])
                                   
        press_text = visual.TextStim(win, text="PRESS\n NOW",
                                   height=25,
                                   alignHoriz='center',
                                   bold=True,
                                   wrapWidth = width,
                                   color = 'yellow') 
                         
        # Show warning and animate fade
        if train_rep==0:
            # Animate (fade-in, hold, and fade-out)
            for i in np.array(range(-100,100,15)+[100]*10+range(100,-100,-20))/100.0:
                    warn_img.mask = np.ones((2**10,2**10), np.uint8)*i
                    warn_img.draw()
                    win.flip()

        # Show 1st block of instructions        
        text = visual.TextStim(win,height=48,
                                   text="When you see this sign...",
                                   pos=[0,height/4],
                                   wrapWidth = width,
                                   alignHoriz='center')
        # Animate face halo
        cont_step = -.1
        cont_out = 1.0  
        curr_time = time.time()
        
        while (time.time()-curr_time) < 3:
        
            # Oscillate img contrast
            cont_out = cont_out + cont_step
            if (cont_out<-.9) or (cont_out>.9):
                cont_step *= -1
            dec_hl_img.contrast = cont_out
            
            # Draw everything to the screen and post
            text.draw()
            dec_hl_img.draw()
            dec_img.draw()
            win.flip()
        
            # Break if 'start' or 'space' is pressed
            if joy.Start() or (' ' in keyboard.getPresses()):
                vid_play = False
                repeat_demo = False
                
                # Acknowledge button press with sound
                laserSound()
                
                break
        
        if vid_play==False:
            break 
          
        # Animate text
        for i in scaled_logDist:
            text.contrast = i 
            text.draw()
            dec_img.contrast = i
            dec_img.draw()
            win.flip()
            
            # Break if 'start' or 'space' is pressed   
            if joy.Start() or (' ' in keyboard.getPresses()):
                vid_play = False
                repeat_demo = False
                
                # Acknowledge button press with sound
                laserSound()
                
                break
            
        if vid_play==False:
            break                         
                                      
        # Show 2nd block of instructions        
        text = visual.TextStim(win,height=48,
                                   text="Identify which of the following\n4 people you see or hear...",
                                   wrapWidth = width,
                                   antialias=True,
                                   alignHoriz='center')
        text.draw()    
        win.flip()
                
        # Pause for reading
        curr_time = time.time()
        while time.time()-curr_time < 3.5:
            # Check keyboard for button presses
            keys = keyboard.getPresses()
            # Check joystick for button presses    
            if joy.Start() or (' ' in keys):
                vid_play = False
                repeat_demo = False
                
                # Acknowledge button press with sound
                laserSound()
                
                break
        
        if vid_play==False:
            break
        
        # Animate fade
        for i in scaled_logDist:
            text.contrast = i 
            text.draw()    
            win.flip()
            
            # Check keyboard for button presses
            keys = keyboard.getPresses()
            # Check joystick for button presses    
            if joy.Start() or (' ' in keys):
                vid_play = False
                repeat_demo = False
                
                # Acknowledge button press with sound
                laserSound()
                
                break
            
        if vid_play==False:
            break
                
        for i in range(len(videolist)):
            
            img = visual.ImageStim(win=win,
                                   image=img_list_button[i],
                                   units="pix")
            if side=='R':
                img.size *= .45  # Scale the image relative to initial size
            else:
                img.size -= img.size/4  # Scale the image relative to initial size
                img.ori += 90*i # Iterate image orientation (rotation)

            if side=='R':
                cue_img = img
            else:
                cue_img = visual.ImageStim(win=win,
                                           image=img_list_cue[i],
                                            units="pix")
                cue_img.size -= cue_img.size/4  # Scale the image relative to initial size
                cue_img.ori += 90*i # Iterate image orientation (rotation)
            
            # Create movie stim by loading movie from list
            mov = visual.MovieStim3(win, videolist[i]) 
            mov.size *= .75  # Scale the image relative to initial size
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
                
                # Check joystick and keyboard for button presses    
                if joy.Start() or (' ' in keyboard.getPresses()):
                    mov.status = visual.FINISHED
                    vid_play = False
                    repeat_demo = False
                    
                    # Acknowledge button press with sound
                    laserSound()
                
                    break
            
            if vid_play==False:
                break
            
            ## Cue button press
            press_text.pos = img_pos_list[i]                
            press_text.contrast = 1  
        
            # Instruct user to press 'Start' and wait on button press
            while cmd_list[i]()==0:
            
                time.sleep(.05)
                
                # Oscillate text contrast while we wait
                if press_text.contrast:
                    press_text.contrast = 0
                else:
                    press_text.contrast = 1
                
                press_text.draw()    
                cue_img.draw()
                mov.draw()
                instr_text.draw()
                fin_text.draw()
                win.flip()
                
                # Check joystick and keyboard for button presses 
                if joy.Start() or (' ' in keyboard.getPresses()):
                    vid_play = False
                    
                    # Acknowledge button press with sound
                    laserSound()
                
                    break
                        
            ## If trial break variable is set, break trial
            if vid_play==False:
                break
                
            # Current Trial is Done
            # Wait on button presses
            t_start = time.time()+1
            while time.time()<t_start:
                # Check joystick and keyboard for button presses    
                if joy.Start() or (' ' in keyboard.getPresses()):
                        vid_play = False
                        
                        # Acknowledge button press with sound
                        laserSound()
                
                        break
                    
        # Prompt user for response (repeat y/n?)
        color_list = ['yellow','grey']
        sw = 0
        curr_time = time.time()
        delay = 1

        while vid_play:
            
            if time.time()-curr_time > delay:
                # Flip switch                        
                sw = 1-sw
                curr_time = time.time()
                
            wait_img = visual.ImageStim(win=win, image=wait_img_list[sw], units="pix")
#            wait_img.size *= .75  # Scale the image relative to initial size
            wait_img.pos = [0, -height/4]
            
            # Text to repeat or proceed
            loop_text_rep = visual.TextStim(win, text="Repeat training?",
                                   height=40,
                                   color=color_list[1-sw],
                                   alignHoriz='center',
                                   wrapWidth = width,
                                   antialias=True,
                                   pos = [-width/5, height/4])
    
            loop_text_proc = visual.TextStim(win, text="Proceed to mission",
                                   height=40,
                                   color=color_list[sw],
                                   alignHoriz='center',
                                   wrapWidth = width,
                                   antialias=True,
                                   pos = [width/5, height/4]) 
                                   
            loop_text_rep.draw()    
            loop_text_proc.draw()
            wait_img.draw()
            
            win.flip()
             
            # Check joystick and keyboard for button presses                      
            if joy.Back():
                break
            elif joy.Start() or (' ' in keyboard.getPresses()):
                repeat_demo = False
                
                # Acknowledge button press with sound
                laserSound()
                
                break
        
        # Iterate training demo counter
        train_rep += 1
        
        # If trial break variable is set, break trial
        if vid_play==False:
            break
        
    ## End 
