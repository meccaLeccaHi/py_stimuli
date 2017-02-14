'''
Simple iohub eye tracker movie player. Presentation of movies is contingent on
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
from psychopy import core, visual
from psychopy.iohub.client import launchHubServer

# Force psychopy to use particular audio library
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

import glob, time, csv, datetime, gtk
import numpy as np
#import struct
from inputs import get_gamepad

# Start screen function
def start_screen( win, start ):

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
        events = get_gamepad()
        for event in events:
            if event.state==1 and event.code==start:
                break
        if event.code==start:
            # Stop music
            if MUSIC:
                filesound.stop()
            break
        
# Give subject instructions
def instruct_screen( win, start ):
    
    # Play music
    if MUSIC:
        filesound = sound.Sound(value = "mission-briefing.wav")
        filesound.setVolume(.1)
        filesound.play()
    
    start_pos = np.array([0, -200.0])  # [x, y] norm units in this case where TextSTim inherits 'units' from the Window, which has 'norm' as default.
    end_pos = np.array([0, 200.0])
    animation_duration = 100  # duration in number of frames
    step_pos = (end_pos - start_pos)/animation_duration
    
    text_str = "dun "*10
    
    # Set up psychopy stuff
#    win = visual.Window()
    text = visual.TextStim(win, text=text_str, height = 50, antialias=True)
    fin_text = visual.TextStim(win, text="Press <Start> to proceed",
                               pos = [0, -(height/2)+50],
                               height = 50,
                               wrapWidth = width,
                               antialias=False,
                               bold=True,
                               italic=True,
                               alignHoriz='center')
                               
    img = visual.ImageStim(win=win, image="stars.jpg", units="pix")
#    img.size *= SCALE  # scale the image relative to initial size
    
    # Animate
#    text.width = 60
    text.pos = start_pos
    for i in range(animation_duration):
        text.pos += step_pos  # add to existing value
        img.draw()
        text.draw()    
        win.flip()
        if RECORD:
            # store an image of every upcoming screen refresh:
            win.getMovieFrame(buffer='back')
        
    # Instruct user to press 'Start'
    img.draw()
    text.draw()
    fin_text.draw()    
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')
        
    # Wait on 'Start' button press
    while True:
           
        events = get_gamepad()
        for event in events:
            if event.state==1 and event.code==start:
                # Animate
                text.contrast = 1
                for i in np.array(range(100,-100,-4))/100.0:
                    text.contrast = i
                    fin_text.contrast = i
                    img.draw()
                    text.draw()
                    fin_text.draw()
                    win.flip()
                    if RECORD:
                        # store an image of every upcoming screen refresh:
                        win.getMovieFrame(buffer='back')
                break
        if (event.state==1 and event.code==start) or (' ' in keyboard.getPresses()):
            # Stop music
            if MUSIC:
                filesound.stop()
            break
        
def readySet( win ):
    
    if MUSIC:#            text_stim.draw()

            filesound = sound.Sound(value = "beep.wav")
            filesound.setVolume(.1)
            
    for i in range(3,0,-1):
        
        if MUSIC:   
            filesound.play()
        
        # Show count-down        
        text = visual.TextStim(win, height=48, text=(str(i)))
    
        # Animate
        text.contrast = 1
        for i in np.array(range(100,-100,-2))/100.0:
            text.contrast = i 
            text.draw()    
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
    
    # Show "Go!"
    text = visual.TextStim(win, height=48, text="Go!")
    text.draw()    
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')

# Joystick response function
def poll_buttons( delay ):
    
    curr_time = time.time()
    resp = None
    resp_time = None
    time_left = 0
    
    # Draw decision cue in window
    dec_img.draw()
    tr_text.draw()
    tr_rect.draw()
    if JOYSTICK:
        prog_bar.draw()
        corr_bar.draw()
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')

    while time.time()-curr_time < delay:
        events = get_gamepad()

        for event in events:
            if event.state==1 and event.code in joy_hash:
#                print(event.ev_type, event.code, event.state)
                resp = joy_hash[event.code]
                resp_time = time.time()-curr_time
                time_left = delay - resp_time
                break
        if resp!= None:
            if resp==IDENT_LIST[trial_num]:
                CORRECT[trial_num] = 1
                right_img.draw()
            else:
                CORRECT[trial_num] = 0
                wrong_img.draw()
            tr_text.draw()
            tr_rect.draw()
            if JOYSTICK:
                prog_bar.draw()
                corr_bar.draw()
            win.flip()
            if RECORD:
                # store an image of every upcoming screen refresh:
                win.getMovieFrame(buffer='back')
            time.sleep(time_left)
            break
        del events
    
    return resp, resp_time

# Save log file function    
def save_logs():
    # Create header array from lists
    head = zip(np.arange(TRIAL_COUNT)+1,new_order+1,videolist,SCR_OPEN,SCR_CLOSE,ISI_END,IDENT_LIST,RESP,RESP_TIME,CORRECT)

    # Write header array to csv file
    with open(headerpath + header_nm + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for val in head:
            writer.writerow(val)
        
    # Tell user about saved header
    print "Header file saved: " + header_nm
    
# Give subject instructions
def end_screen( win, start ):
    
    break_endscr = False
    
    # Play music
    if MUSIC:
        filesound = sound.Sound(value = "stage_clear.wav")
        filesound.setVolume(.1)
        filesound.play()
    
    text_str = "Your final score was: {}% correct\n\n Play again?".format(ave_str)
    
    # Set up psychopy stuff
#    win = visual.Window()
    text = visual.TextStim(win, text=text_str, height=50, alignHoriz='center')                          
    img = visual.ImageStim(win=win, image="stars.jpg", units="pix")
#    img.size *= SCALE  # scale the image relative to initial size
            
    # Instruct user to press 'Start'
    img.draw()
    text.draw()    
    win.flip()
    if RECORD:
        # store an image of every upcoming screen refresh:
        win.getMovieFrame(buffer='back')
        
    # Wait on 'Start' button press
    while break_endscr==False:
                
        # Check keyboard for button presses
        keys = keyboard.getPresses()
        # Check joystick for button presses    
        events = get_gamepad()
        for event in events:
            if (event.state==1 and event.code==start) or (' ' in keys):
                # Animate
                text.contrast = 1
                for i in np.array(range(100,-100,-4))/100.0:
                    text.contrast = i
                    img.draw()
                    text.draw()
                    win.flip()
                    if RECORD:
                        # store an image of every upcoming screen refresh:
                        win.getMovieFrame(buffer='back')
                if MUSIC:
                    filesound.stop()
                break_exp = False
                break_endscr = True
                break
            elif ('q' in keys):
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
    
# Find movies matching wildcard search
videopath = '/home/adam/Desktop/py_stimuli/JonesStimset/'
videolist = glob.glob(videopath + '*.avi')
videolist = videolist[0:5]

# Set header path and file name (according to current time)
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
JOYSTICK = 1; # 1: yes, 0: no
# Boolean for intro music
MUSIC = 1; # 1: yes, 0: no

# Create hash table for joystick inputs
joy_hash = {}
joy_hash['BTN_TRIGGER'] = 0
joy_hash['BTN_THUMB'] = 1
joy_hash['BTN_THUMB2'] = 2
joy_hash['BTN_TOP'] = 3

start = 'BTN_BASE4'
    
# Include/remove noise controls
if CONTROLS==0:
    videolist = [x for x in videolist if not 'noisy' in x]
    
# Total trial count for experiment
TRIAL_COUNT = len(videolist) * BLOCK_REPS

# Set screen parameters
if TESTING:
    FLSCRN = False
    # Scale screen for testing
    SCREEN_SIZE = np.array([(x/3) for x in (width, height)])
    # We're referencing pixels, so must be in integer values
    SCREEN_SIZE = np.floor(SCREEN_SIZE)
else:
    FLSCRN = True
    SCREEN_SIZE = np.array([width, height])
    
# Set up photodiode
PHOTO_SIZE = 50
# Pixels must be integers
PHOTO_POS = np.floor((SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1])

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
display = io.devices.display
    
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
    break_block = False
    # Extract identity numbers from video list
    ident_ind = videolist[0].find("identity")+len("identity")
    IDENT_LIST = np.unique([x[ident_ind] for x in videolist],return_inverse = True)[1]
    
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
        
        # Display start screen and wait for user to press 'Start'
        start_screen(win, start)
        # Display instruction screen, then wait for user to press 'Start'
        instruct_screen(win, start)
        
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
            corr_move = height*((average-100)/100.0)
            corr_bar = visual.Rect(win = win, width=75, height=height,
                    pos = [-(width/2),0+corr_move], fillColor = 'red', lineColor = 'red')
                                                  
        tr_text = visual.TextStim(win, text=(str(trial_num+1)))
        tr_rect = visual.Rect(win, width=tr_text.boundingBox[0], height=tr_text.boundingBox[1])
        tr_text.pos = [(width/2)-tr_text.boundingBox[0],(height/2)-tr_text.boundingBox[1]]     
        tr_rect.pos = [(width/2)-tr_text.boundingBox[0],(height/2)-tr_text.boundingBox[1]]      
                  
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win, videolist[trial_num]) 
        
        io.clearEvents()
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
            if 'q' in keys:
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
        else:
            # Pause for n seconds
            time.sleep(delay)
            
        # Log ISI end time for header
        ISI_END[trial_num] = core.getTime()
    
    ## Save log files    
    save_logs()
    
    # All Trials are done
    break_exp = end_screen( win, start )
    
    if RECORD:
        # Combine movie frames in a  movie file
        win.saveMovieFrames(fileName='mov_file.mp4')
    
if EYE_TRACKER:
    tracker.setConnectionState(False)
       
## End experiment
io.quit()
core.quit()