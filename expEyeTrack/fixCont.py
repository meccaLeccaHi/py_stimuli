'''
Iohub eye-tracking/joystick-compatible movie player. 
Presentation of movies can be contingent on
central fixation.
No iohub config .yaml files are used.
Setup for an EyeLink(C) 1000 Desktop System. 
To to use a different eye tracker implementation, change the 
iohub_tracker_class_path and eyetracker_config dict script variables.
Currently loading raw (uncompressed) videos, 
future versions should read compressed movies-
    video: H.264 compressed,
    audio: Linear PCM
'''

#from constants import DISPSIZE

from psychopy import core, visual
from psychopy.iohub.client import launchHubServer

# Force psychopy to use particular audio library
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

import glob, time, csv, datetime, gtk, xbox # , subprocess, os
import numpy as np

# Import custom functions
from buttonDemo import buttonDemo
from plot_beh import plot_beh

# Start screen function
def start_screen( win ):

    img = visual.ImageStim(win=win, image="start_screen.png",
                                    units="pix")
#    img.size *= SCALE  # scale the image relative to initial size

    # Draw the image to window and show on screen
    img.draw()
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')
    
    # Play music
    if MUSIC:
        filesound = sound.Sound(value = "theme.wav")
        filesound.setVolume(.1)
        filesound.play() 

    # Wait on 'Start' button press
    while True:
        if joy.Start():
            # Stop music
            if MUSIC:
                filesound.stop()
            break
        
# Give subject instructions
def instruct_screen( win ):
    
    instruct_play = True
    
    # Play music
    if MUSIC:
        filesound = sound.Sound(value = "mission-briefing.wav")
        filesound.setVolume(.1)
        filesound.play()
        
    instr_img = visual.ImageStim(win=win, image="instructions.png",
                                    units="pix")
    #    img.size *= SCALE  # scale the image relative to initial size
    
    start_pos = np.array([0, -height/3])  # [x, y] norm units in this case where TextSTim inherits 'units' from the Window, which has 'norm' as default.
    end_pos = np.array([0, -height/20.0])
    animation_duration = 300  # duration in number of frames
    step_pos = (end_pos - start_pos)/animation_duration
                           
    fin_text = visual.TextStim(win=win, text="Press <Start> to proceed",
                               pos = [0, -(height/2)+50],
                               height = 50,
                               wrapWidth = width,
                               antialias=False,
                               italic=True,
                               alignHoriz='center')
    
    # Create background image                           
    img = visual.ImageStim(win=win, image="stars.jpg", units="pix")
#    img.size *= SCALE  # scale the image relative to initial size
    
    # Animate
    instr_img.pos = start_pos
    for i in range(animation_duration):
        instr_img.pos += step_pos  # Add to existing value
        # Draw images to window and show on screen
        img.draw()
        instr_img.draw()
        win.flip()
        if RECORD:
            # Store image of upcoming screen refresh
            win.getMovieFrame(buffer='back')
            
        if joy.Start() or (' ' in keyboard.getPresses()):
            instruct_play = False
            break
    
    cont_step = -.1
    cont_out = 1.0  
    
    # Instruct user to press 'Start' and wait on button press
    while (instruct_play):
        
        # Oscillate text contrast while we wait
        cont_out = cont_out + cont_step
        if (cont_out<-.9) or (cont_out>.9):
            cont_step *= -1
        fin_text.contrast = cont_out

        # Draw everything to the screen and post
        img.draw()
        instr_img.draw()
        fin_text.draw()
        time.sleep(.01)
        win.flip()
        if RECORD:
            # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
        
        # Break if 'start' or 'space' is pressed
        if joy.Start() or (' ' in keyboard.getPresses()):
            instruct_play = False
            break

    # Stop music
    if MUSIC:
        filesound.stop()
                
def readySet( win ):
    
    if MUSIC:
            filesound = sound.Sound(value="beep.wav")
            filesound.setVolume(.1)
            
    # Show "Mission starting in:"
    text_start = visual.TextStim(win=win,
                                 height=30,
                                 pos = [0, height/6],
                                 text="Mission starting in:")
                                     
    for i in range(3,0,-1):
        
        # Play sound
        if MUSIC:   
            filesound.play()
        
        # Show count-down        
        text = visual.TextStim(win,height=48,bold=True,text=str(i))
    
        # Animate
        for i in np.array(range(100,-100,-2))/100.0:
            text.contrast = i 
            text_start.draw()
            text.draw()    
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
    
    # Show "Go!"
    text = visual.TextStim(win,height=48,bold=True,text="Go!")
    text.draw()    
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')
    time.sleep(.25)
    
def segue( win ):
    
    # Play sound
    if MUSIC:
            filesound = sound.Sound(value = "morse.wav")
            filesound.setVolume(.1)
            filesound.play()
            
    # Load background image
    img = visual.ImageStim(win=win, image="stars.jpg", units="pix")

    # Show message        
    text_str = "Incoming transmissions for {}...".format(user_name)
    text = visual.TextStim(win, height = 30,
                               wrapWidth = width,
                               antialias=True,
                               alignHoriz='center',
                               text=text_str)

    # Animate
    text.contrast = 1
    for i in np.array(range(100,-100,-2))/100.0:
        text.contrast = i
        img.draw()
        text.draw()    
        win.flip()
        if RECORD:
            # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
    
    time.sleep(.4)

# Joystick response function
def poll_buttons( delay ):
    
    curr_time = time.time()
    resp = None
    resp_time = None
    time_left = 0
    
    # Draw decision cue in window and post to screen
    dec_img.draw()
    tr_text.draw()
    tr_rect.draw()
    prog_bar.draw()
    corr_bar.draw()
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')

    while time.time()-curr_time < delay:
        if joy.dpadUp():
            resp = 0
        elif joy.dpadRight():
            resp = 1
        elif joy.dpadDown():
            resp = 2
        elif joy.dpadLeft():
            resp = 3
            
        if resp!= None:
            resp_time = time.time()-curr_time
            time_left = delay - resp_time
            
            # Draw everything and post to screen
            if resp==IDENT_LIST[trial_num]:
                CORRECT[trial_num] = 1
                right_img.draw()
            else:
                CORRECT[trial_num] = 0
                wrong_img.draw()    
            tr_text.draw()
            tr_rect.draw()
            prog_bar.draw()
            corr_bar.draw()
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
                
            time.sleep(time_left)
            break
    
    return resp, resp_time

# Save log file function    
def save_logs():
    # Create header array from lists
    head = zip(np.arange(TRIAL_COUNT)+1,new_order+1,videolist,SCR_OPEN,SCR_CLOSE,ISI_END,IDENT_LIST,RESP,RESP_TIME,CORRECT,TRAJ_LIST,STEP_LIST)

    # Write header array to csv file
    with open(headerpath + header_nm + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for val in head:
            writer.writerow(val)
        
    # Tell user about saved header
    print "Header file saved: " + header_nm
    
# Give subject feedback at end of each trial
def end_screen( win, beh_fig_name ):
    
    break_endscr = False
    
    # Play music
    if MUSIC:
        filesound = sound.Sound(value = "tyson.wav")
        filesound.setVolume(.4)
        filesound.play()
    
    text_str = user_name + "'s score:"
    corr_str = "{}%".format(ave_str)
    
    # Set up psychopy stuff
    text = visual.TextStim(win, text=text_str,
                           height=50,
                           alignHoriz='center',
                           wrapWidth = width,
                           pos = [0, height/3])
    score_text = visual.TextStim(win, text=corr_str,
                           height=70,
                           color=barCol,
                           alignHoriz='center',
                           bold=True,
                           wrapWidth = width,
                           pos = [width/6, 0])
    fin_text = visual.TextStim(win, text="Play again? <Press Start>",
                           height=50,
                           alignHoriz='center',
                           italic=True,
                           wrapWidth = width,
                           pos = [0, -height/2.5])                          
    img = visual.ImageStim(win=win, image="stars.jpg", units="pix")
#    img.size *= SCALE  # scale the image relative to initial size
    
    beh_img = visual.ImageStim(win=win,
                               image = beh_fig_name,
                               units = "pix",
                               pos = [-width/6, 0])
#    beh_img.size *= .75  # scale the image relative to initial size

    # Instruct user to press 'Start'
        
    cont_step = -.1
    cont_out = 1.0 
        
    # Wait on 'Start' button press
    while break_endscr==False:
        
        # Oscillate text contrast while we wait
        cont_out = cont_out + cont_step
        if (cont_out<-.9) or (cont_out>.9):
            cont_step *= -1
        fin_text.contrast = cont_out

        # Draw everything and post to screen
        img.draw()
        beh_img.draw()
        text.draw()
        score_text.draw()
        fin_text.draw()
        win.flip()
        if RECORD:
        # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
        
        # Check devices for button presses
        keys = keyboard.getPresses()
        if joy.Start() or (' ' in keys):       
            # Acknowledge button press with sound
            if MUSIC:
                filesound.stop()
                filesound = sound.Sound(value = "yes.wav")
                filesound.setVolume(.5)
                filesound.play()
                
            # Animate
            text.contrast = 1
            for i in np.array(range(100,-100,-4))/100.0:
                text.contrast = i
                beh_img.contrast = i                
                img.draw()
                beh_img.draw()
                text.draw()
                win.flip()
                if RECORD:
                    # store an image of every upcoming screen refresh:
                    win.getMovieFrame(buffer='back')
                
            break_exp = False
            break_endscr = True
            
            break
        elif joy.Back() or ('q' in keys):
            # Stop music
            if MUSIC:
                filesound.stop()
            break_exp = True
            break_endscr = True
            break
    return break_exp



## Start script
# Initialize boolean to break and end experiment
break_exp = False

## Initialize variables

# Counter
play_reps = 0

# Define path for figure output
fig_dir = "/home/adam/Desktop/py_stimuli/expEyeTrack/beh_figs/"
    
# Find movies matching wildcard search
videopath = '/home/adam/Desktop/py_stimuli/JonesStimset/'
videolist = glob.glob(videopath + '*.avi')
#videolist = videolist[0:5]

# Set header path
headerpath = '/home/adam/Desktop/py_stimuli/expEyeTrack/headers/'

 # Get current screen size (works for single monitor only)
width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()
    
# Number of trials of each stimulus to run
BLOCK_REPS = 1
# Inter-stimulus interval (seconds)
ISI = 1
# Jitter range (+/-seconds)
JITTER = .1
# Scaling of image (none = 1)
SCALE = 1

# Boolean for debugging mode
TESTING = 0; # 1: yes, 0: no
# Boolean for recording screen frames to movie output
RECORD = 0; # 1: yes, 0: no
# Boolean for including control stimuli
CONTROLS = 0; # 1: yes, 0: no
# Boolean for presence of tracker
EYE_TRACKER = 0; # 1: yes, 0: no
# Boolean to simulate tracker activity with mouse
SIMULATE = 1; # 1: yes, 0: no
# Boolean for presence of joystick (N64 only, currently)
JOYSTICK = 1; # 1: yes, 0: no1
# Boolean for intro music
MUSIC = 1; # 1: yes, 0: no

if JOYSTICK:
    # Initialize joystick device
    joy = xbox.Joystick()
    
# Include/remove noise controls
if CONTROLS==0:
    videolist = [x for x in videolist if not 'noisy' in x]
    
# Total trial count for experiment
TRIAL_COUNT = len(videolist) * BLOCK_REPS

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
    
# Set up photodiode
PHOTO_SIZE = 50
# Pixels must be integers
PHOTO_POS = np.floor((SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1])

# Prompt for player name
user_name = "Agent " + raw_input('Enter player\'s name [e.g. Fabio]: ').title()

## Create window
win = visual.Window(SCREEN_SIZE.tolist(),
                    units='pix',
                    fullscr=FLSCRN,
                    allowGUI=False,
                    color='black', 
                    winType='pyglet')
                        
## Initialize devices    
if EYE_TRACKER:
    # Set up eye-tracker configuration dict
    iohub_tracker_class_path = 'eyetracker.hw.sr_research.eyelink.EyeTracker'
    eyetracker_config = dict()
    eyetracker_config['name'] = 'tracker'
    if SIMULATE:
        eyetracker_config['simulation_mode'] = True
    else:
        eyetracker_config['model_name'] = 'EYELINK 1000 DESKTOP'
        eyetracker_config['runtime_settings'] = dict(sampling_rate=1000, 
            track_eyes='RIGHT')

    # Since no experiment or session code is given, no iohub hdf5 file
    # will be saved, but device events are still available at runtime
    io = launchHubServer(**{iohub_tracker_class_path: eyetracker_config})
    # Get iohub device for tracker
    tracker = io.devices.tracker
else:
    io = launchHubServer()

# Get devices for future access
keyboard = io.devices.keyboard
#display = io.devices.display
    
if EYE_TRACKER:
    # Run eyetracker calibration
    r = tracker.runSetupProcedure()

while break_exp==False:
    
    # Initialize boolean to break and end experiment
    break_block = False
    
    # Set header path and file name (according to current time)
    header_nm = 'hdr'+datetime.datetime.now().strftime("%m%d%Y_%H%M")
        
    # Create new stimulus order for entire experiment
    perm_list = [ np.random.permutation(len(videolist)) for i in range(BLOCK_REPS) ]
    new_order = np.concatenate(perm_list)
        
    # Re-order (and grow, if necessary) stimulus list
    videolist = [ videolist[i] for i in new_order ]

    # Extract identity numbers from video list
    ident_ind = videolist[0].find("identity")+len("identity")
    IDENT_LIST = np.unique([x[ident_ind] for x in videolist],return_inverse = True)[1]
    
    # Correct identity # for faces more than 50% along tang. trajectory
    TRAJ_LIST = np.unique([x[ident_ind+1:ident_ind+4] for x in videolist],return_inverse = True)[1]
    STEP_LIST = np.unique([x[ident_ind+5:ident_ind+8] for x in videolist],return_inverse = True)[1]
    temp1 = IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST<=1))]
    temp2 = temp1.copy()
    temp2[temp1<max(temp1)] += 1
    temp2[temp1==max(temp1)] = 0
    IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST<=1))] = temp2
    
    # Create jitter times (uniformly distributed)
    jitter_times = np.random.uniform(-JITTER, JITTER, TRIAL_COUNT)
    
    # Pre-allocate timing lists
    SCR_OPEN = [None] * TRIAL_COUNT
    SCR_CLOSE = [None] * TRIAL_COUNT
    ISI_END = [None] * TRIAL_COUNT
    
    # Pre-allocate response list
    RESP = [None] * TRIAL_COUNT
    RESP_TIME = [None] * TRIAL_COUNT
    CORRECT = [None] * TRIAL_COUNT
    CORRECT[0] = 0 # Initialize with zero so the running average works at the beginning  
        
    # Define window objects
    if JOYSTICK:
        
        if play_reps==0:
            # Display start screen and wait for user to press 'Start'
            start_screen(win)
        play_reps += 1
        
        # Display 'incoming transmission' segue
        segue(win)
        # Display instruction screen, then wait for user to press 'Start'
        instruct_screen(win)
        # Display demonstration of identities and corresponding dpad directions
            # Initialize devices for future access
     
        # Run demo on button-identity mapping
        buttonDemo(win, joy, keyboard)
        
        # Create relevant image stimuli
        dec_img = visual.ImageStim(win=win,image="decision.png",units="pix")
        right_img = visual.ImageStim(win=win,image="right.png",units="pix")
        wrong_img = visual.ImageStim(win=win,image="wrong.png",units="pix")
    
    # Countdown to start
    readySet( win )
    
    # Set up eye-tracker visual objects
    if EYE_TRACKER:
        gaze_ok_region = visual.Circle(win, radius=200, units='pix')
        gaze_dot = visual.GratingStim(win, tex=None, mask='gauss', pos=(0, 0),
                                  size=(33, 33), color='green', units='pix')
    # Set up feedback bar
    if JOYSTICK:
        prog_bar = visual.Rect(win = win, width=75, height=height,
                    pos = [-(width/2),0], fillColor = 'grey', lineColor = 'grey')
     
    # Create photodiode patch               
    photodiode = visual.GratingStim(win, tex=None, mask='none', pos=PHOTO_POS.tolist(),
                                    size=100)
                                    
        
    ## Launch experiment                                 
    globalClock = core.Clock()  # to track the time since experiment started
    
    # Run Trials.....
    for trial_num in range(TRIAL_COUNT):
        
        # Get current average percent correct
        average = int(np.mean([x for x in CORRECT if x is not None])*100)   
        ave_str = str(average)
        
        if JOYSTICK:
            # Set color of '% correct bar'
            corr_move = height*((average-100)/100.0)
            if average<=25:
                barCol = 'red'
            elif average<=50:
                barCol='yellow'
            else:
                barCol='green'
            # Create '% correct bar'
            corr_bar = visual.Rect(win=win, width=75, height=height,
                    pos=[-(width/2),0+corr_move], fillColor=barCol, lineColor=barCol)
                                                  
        tr_text = visual.TextStim(win, text=(str(trial_num+1)))
        tr_rect = visual.Rect(win, width=tr_text.boundingBox[0], height=tr_text.boundingBox[1])
        tr_text.pos = [(width/2)-tr_text.boundingBox[0],(height/2)-tr_text.boundingBox[1]]     
        tr_rect.pos = tr_text.pos      
                  
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win, videolist[trial_num]) 
        
#        io.clearEvents()
        if EYE_TRACKER:
            tracker.setRecordingState(True)
        
        # Add timing of movie opening to header
        SCR_OPEN[trial_num] = core.getTime()
            
        # Start the movie stim by preparing it to play
        shouldflip = mov.play()
            
        # If boolean to finish current movie AND movie has not finished yet
        while mov.status != visual.FINISHED:
            
            # if tracker is on
            if EYE_TRACKER:
                # Get the latest gaze position in display coord space
                gpos = tracker.getLastGazePosition()
            
                # Update stim based on gaze position
                valid_gaze_pos = isinstance(gpos, (tuple, list))
                gaze_in_region = valid_gaze_pos and gaze_ok_region.contains(gpos)
            else: # else ignore
                valid_gaze_pos = True
                gaze_in_region = True
    
            # If we have a gaze position from the tracker,
            # test whether subject is fixating
            if valid_gaze_pos:
                
                # Update movie and text stim
                if gaze_in_region:
                    gaze_in_region = 'Yes'
                            
                    # Draw movie stim again
                    shouldflip = mov.draw()
                    
                    # Draw photodiode patch
                    photodiode.draw()
                    
                else:
                    # If gave leaves region, end trial
                    gaze_in_region = 'No'
                    mov.status = visual.FINISHED
                            
                #trial_num = t + block * len(videolist)
                # Update text on screen
                if EYE_TRACKER:
                    gaze_dot.setPos(gpos)
    
            # Redraw screen without movie stimuli
            if EYE_TRACKER:
                gaze_ok_region.draw()
            tr_text.draw()
            tr_rect.draw()
            if JOYSTICK:
                prog_bar.draw()
                corr_bar.draw()
            
            if valid_gaze_pos:
                if EYE_TRACKER:
                    gaze_dot.draw()
            
            # Display updated stim on screen
            flip_time = win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
            
            # Check keyboard for button presses
            keys = keyboard.getPresses()
    
            # Check any new keyboard char events for a space key
            # If one is found, set the trial end variable
            if ' ' in keys:
                mov.status = visual.FINISHED
                
            # Check any new keyboard char events for a 'q' key
            # If one is found, set the experiment break boolean
            if joy.Back() or ('q' in keys):
                break_exp = True
                break_block = True
                break
                # in the future- this can run some method to save the header then "exit(0)"
        
        # Current Trial is Done
        # If trial break variable is set, break trial
        if break_block:
            break
        
        # Current Trial is Done
        
        # Redraw stim
        if EYE_TRACKER:
            gaze_ok_region.draw()
        tr_text.draw()
        tr_rect.draw()
        if JOYSTICK:
            prog_bar.draw()
            corr_bar.draw()
        
        # Display updated stim on screen
        flip_time = win.flip(clearBuffer=True)
        
        # Log movie end time for header
        SCR_CLOSE[trial_num] = core.getTime()
            
        if EYE_TRACKER:
            # Stop eye data recording
            tracker.setRecordingState(False)
         
        delay = ISI + jitter_times[trial_num]
        
        # Check joystick for button presses
        if JOYSTICK:
            # Poll joystick for n seconds
            RESP[trial_num], RESP_TIME[trial_num] = poll_buttons(delay)
        
        # Pause for n seconds
        tr_text.draw()
        tr_rect.draw()
        if JOYSTICK:
            prog_bar.draw()
            corr_bar.draw()
        win.flip(clearBuffer=True)
        time.sleep(delay)
            
        # Log ISI end time for header
        ISI_END[trial_num] = core.getTime()
    
    ## Save log files    
    save_logs()
    
#    win.close()
#    ## Save psychometric figs
    plt = plot_beh(STEP_LIST,TRAJ_LIST,CORRECT,rad_only=True,SCORE=average)
    figOut_name = fig_dir + "beh_fig_" + header_nm + ".png"    
    plt.savefig(filename=figOut_name,
                dpi=100, transparent=True)
    plt.close()
    
    # All Trials are done
    break_exp = end_screen( win, figOut_name )
    
    if RECORD:
        # Combine movie frames in a  movie file
        win.saveMovieFrames(fileName='mov_file.mp4')
    

## End experiment   
win.close() 
if EYE_TRACKER:
    tracker.setConnectionState(False)
if JOYSTICK:
    joy.close()
io.quit()
core.quit()