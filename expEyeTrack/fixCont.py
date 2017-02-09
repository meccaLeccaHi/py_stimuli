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

# Define a function for the joystick response
def poll_buttons( delay ):
    
    curr_time = time.time()
    resp = None
    resp_time = None
    time_left = 0
    
    # Draw decision cue to window
    dec_img.draw()
    text_stim.draw()
    win.flip()

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
            text_stim.draw()
            win.flip()
            time.sleep(time_left)
            break
        del events
    
    return resp, resp_time

# Find movies matching wildcard search
videopath = '/home/adam/Desktop/py_stimuli/JonesStimset/'
videolist = glob.glob(videopath + '*.avi')

# Set header path and file name (according to current time)
headerpath = '/home/adam/Desktop/py_stimuli/expEyeTrack/headers/'
header_nm = 'hdr'+datetime.datetime.now().strftime("%m%d%Y_%H%M")

# Number of trials of each stimulus to run
BLOCK_REPS = 1
# Inter-stimulus interval (seconds)
ISI = 1
# Jitter range (+/-seconds)
JITTER = .1
# Scaling of image (none = 1)
SCALE = 1
# Total trial count for experiment
TRIAL_COUNT = len(videolist) * BLOCK_REPS

# Create hash table for joystick inputs
joy_hash = {}
joy_hash['BTN_TRIGGER'] = 0
joy_hash['BTN_THUMB'] = 1
joy_hash['BTN_THUMB2'] = 2
joy_hash['BTN_TOP'] = 3
    
# Create new stimulus order for entire experiment
perm_list = [ np.random.permutation(len(videolist)) for i in range(BLOCK_REPS) ]
new_order = np.concatenate(perm_list)

# Re-order (and grow, if necessary) stimulus list
videolist = [ videolist[i] for i in new_order ]

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
CORRECT[0] = 0

# Boolean for debugging mode
TESTING = 0; # 1: yes, 0: no

# Boolean for presence of tracker
EYE_TRACKER = 0; # 1: yes, 0: no
# Boolean to simulate tracker activity with mouse
SIMULATE = 1; # 1: yes, 0: no

# Boolean for presence of joystick (N64 only, currently)
JOYSTICK = 1; # 1: yes, 0: no

# Get current screen size (works for single monitor only)
width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()

# Set-up screen
if TESTING:
    FLSCRN = False
    # Scale screen for testing
    SCREEN_SIZE = np.array([(x/3) for x in (width, height)])
    # We're referencing pixels, so must be in integer values
    SCREEN_SIZE = np.floor(SCREEN_SIZE)
else:
    FLSCRN = True
    SCREEN_SIZE = np.array([width, height])
    
# Set-up photodiode
PHOTO_SIZE = 50
# Again, we're referencing pixels, so must be in integer values
PHOTO_POS = np.floor((SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1])
    
if EYE_TRACKER:
    # Set-up tracker configuration dict
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

# Create window
win = visual.Window(SCREEN_SIZE.tolist(),
                    units='pix',
                    fullscr=FLSCRN,
                    allowGUI=False,
                    color='black', winType='pyglet'
                    )
    
# Define window objects
dec_img = visual.ImageStim(win=win,image="decision.png",units="pix")
right_img = visual.ImageStim(win=win,image="right.png",units="pix")
wrong_img = visual.ImageStim(win=win,image="wrong.png",units="pix")

gaze_ok_region = visual.Circle(win, radius=200, units='pix')
gaze_dot = visual.GratingStim(win, tex=None, mask='gauss', pos=(0, 0),
                              size=(33, 33), color='green', units='pix')
photodiode = visual.GratingStim(win, tex=None, mask='none', pos=PHOTO_POS.tolist(),
                                size=100)
                                
    
text_stim_str = 'Eye Position: %.2f, %.2f. In Region: %s\n'

missing_gpos_str = 'Eye Position: MISSING. In Region: No\n'
text_stim = visual.TextStim(win, text=text_stim_str,
                            pos=[0, int((-win.size[1]/2)*0.8)], height=24,
                                 color='white',
                                 alignHoriz='center',
                                 alignVert='center', 
                                 wrapWidth=win.size[0] * .9)
                                 
globalClock = core.Clock()  # to track the time since experiment started

# Run Trials.....
#for vidPath in videolist:
for trial_num in range(TRIAL_COUNT):
    
    # Create movie stim by loading movie from list
    mov = visual.MovieStim3(win, videolist[trial_num], size=(366, 332), fps = 30,
                            flipVert=False, flipHoriz=False, loop=False) 
    
    io.clearEvents()
    if EYE_TRACKER:
        tracker.setRecordingState(True)
     
    # Initialize boolean to break and end experiment
    break_exp = False
    
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
                text_stim.text = text_stim_str % (gpos[0], gpos[1], gaze_in_region, trial_num)
                gaze_dot.setPos(gpos)
            else:
                text_stim.text = missing_gpos_str
                            
        else:
            # Otherwise just update text stim
            text_stim.text = missing_gpos_str
        
        if JOYSTICK:
            average = int(np.mean([x for x in CORRECT if x is not None])*100)
            perc_corr_str = "Ave. Correct: {}%\n".format(average)
        else:
            perc_corr_str = ""
        text_stim.text += "Trial Number: {}\n".format(trial_num)
        text_stim.text += perc_corr_str
            
        # Redraw screen without movie stimuli
        gaze_ok_region.draw()
        text_stim.draw()
        if valid_gaze_pos:
            if EYE_TRACKER:
                gaze_dot.draw()
        
        # Display updated stim on screen
        flip_time = win.flip()
        
        # Check keyboard for button presses
        keys = keyboard.getPresses()

        # Check any new keyboard char events for a space key
        # If one is found, set the trial end variable
        if ' ' in keyboard.getPresses():
            mov.status = visual.FINISHED
            
        # Check any new keyboard char events for a 'q' key
        # If one is found, set the experiment break boolean
        if 'q' in keys:
            break_exp = True
            break
            # in the future- this can run some method to save the header then "exit(0)"
    
    # Current Trial is Done
    # If trial break variable is set, break trial
    if break_exp:
        break
    
    # Current Trial is Done
    
    # Redraw stim
    gaze_ok_region.draw()
    text_stim.draw()
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

# All Trials are done
win.close()
if EYE_TRACKER:
    tracker.setConnectionState(False)
    
# Create header array from lists
head = zip(np.arange(TRIAL_COUNT)+1,new_order+1,videolist,SCR_OPEN,SCR_CLOSE,ISI_END,IDENT_LIST,RESP,RESP_TIME,CORRECT)

# Write header array to csv file
with open(headerpath + header_nm + '.csv', 'wb') as f:
    writer = csv.writer(f)
    for val in head:
        writer.writerow(val)
        
# Tell user about saved header
print "Header file saved: " + header_nm
        
# End experiment
io.quit()
core.quit()