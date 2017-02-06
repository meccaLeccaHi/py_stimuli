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

# Manually select audio library for psychopy
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

import glob, time, pygame, csv, datetime, gtk
import numpy as np

# Find movies matching wildcard search
videopath = '/home/adam/Desktop/py_stimuli/JonesStimset/'
videolist = glob.glob(videopath + '*.avi')

# Set header file name (according to current time)
headerpath = '/home/adam/Desktop/py_stimuli/expEyeTrack/headers/'
header_nm = 'hdr'+datetime.datetime.now().strftime("%m%d%Y_%H%M")

# Number of trials of each stimulus to run
BLOCK_REPS = 1
# Inter-stimulus interval (seconds)
ISI = .5
# Jitter range (+/-seconds)
JITTER = .1
# Scaling of image (none = 1)
SCALE = 1
# Total trial count for experiment
TRIAL_COUNT = len(videolist) * BLOCK_REPS

# Create new stimulus order for entire experiment
perm_list = [ np.random.permutation(len(videolist)) for i in range(BLOCK_REPS) ]
new_order = np.concatenate(perm_list)

# Re-order (and grow, if necessary) stimulus list
videolist = [ videolist[i] for i in new_order]

# Create jitter times (uniformly distributed)
jitter_times = np.random.uniform(-JITTER, JITTER, TRIAL_COUNT)

# Create timing lists
SCR_OPEN = [None] * TRIAL_COUNT
SCR_CLOSE = [None] * TRIAL_COUNT
ISI_END = [None] * TRIAL_COUNT
        
# toggle for debugging mode
TESTING = 0; # 1: yes, 0: no

# toggle for presence of tracker
EYE_TRACKER = 0; # 1: yes, 0: no
# toggle to simulate tracker activity with mouse
SIMULATE = 0; # 1: yes, 0: no

# toggle for presence of joystick (N64 only, currently)
JOYSTICK = 0; # 1: yes, 0: no

# Get current screen size (works for single monitor only)
width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()

# Set-up screen
if TESTING:
    FLSCRN = False
    SCREEN_SIZE = floor(np.array([width, height])/3)
else:
    FLSCRN = True
    SCREEN_SIZE = np.array([width, height])
    
# Set-up photodiode
PHOTO_SIZE = 50
PHOTO_POS = (SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1]
    
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
  
if JOYSTICK:
    # Initialize the joystick
    pygame.init()
    pygame.joystick.init()    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Get iohub devices for future access
keyboard = io.devices.keyboard
display = io.devices.display

if EYE_TRACKER:
    # Run eyetracker calibration
    r = tracker.runSetupProcedure()
    
win = visual.Window(SCREEN_SIZE.tolist(),
                    units='pix',
                    fullscr=FLSCRN,
                    allowGUI=False,
                    color='black'
                    )

# Define window objects
gaze_ok_region = visual.Circle(win, radius=200, units='pix')
gaze_dot = visual.GratingStim(win, tex=None, mask='gauss', pos=(0, 0),
                              size=(33, 33), color='green', units='pix')
photodiode = visual.GratingStim(win, tex=None, mask='none', pos=PHOTO_POS.tolist(),
                                size=100)

text_stim_str = 'Eye Position: %.2f, %.2f. In Region: %s\n'
text_stim_str += 'Trial #: %d\n'
text_stim_str += 'Press space key to skip trial.'

missing_gpos_str = 'Eye Position: MISSING. In Region: No\n'
missing_gpos_str += 'Press space key to skip trial.'
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
    
    # Create False variable for joystick button        
    button = 0;
        
    # Create movie stim by loading movie from list
    mov = visual.MovieStim3(win, videolist[trial_num], size=(366, 332), fps = 30,
                            flipVert=False, flipHoriz=False, loop=False) 
    
    io.clearEvents()
    if EYE_TRACKER:
        tracker.setRecordingState(True)
    
    # Initialize boolean to finish current movie
    run_trial = True
    
    # Initialize boolean to break and end experiment
    break_trial = False
    
    # Add timing of movie opening to header
    SCR_OPEN[trial_num] = core.getTime()
        
    # Start the movie stim by preparing it to play
    shouldflip = mov.play()
        
    # Initialize frame counter
    frame_num = 0;
        
    # If boolean to finish current movie AND movie has not finished yet
    while (run_trial is True)&(mov.status != visual.FINISHED):
                
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
                    
                # Only flip when a new frame should be displayed
                if shouldflip:
                    # Movie has already been drawn, so just draw text stim and flip
                    text.draw()
                    win.flip()
                else:
                    # Give the OS a break if a flip is not needed
                    time.sleep(0.001)
                        
                # Draw movie stim again
                shouldflip = mov.draw()
                
                # Draw photodiode patch
                photodiode.draw()
                    
                # Increment frame count
                frame_num += 1
                
            else:
                gaze_in_region = 'No'
                mov.status = visual.FINISHED
                        
            #trial_num = t + block * len(videolist)
            # Update text
            if EYE_TRACKER:
                text_stim.text = text_stim_str % (gpos[0], gpos[1], gaze_in_region, trial_num)
                gaze_dot.setPos(gpos)
            else:
                text_stim.text = missing_gpos_str
                            
        else:
            # Otherwise just update text stim
            text_stim.text = missing_gpos_str
        
        # Redraw stim
        gaze_ok_region.draw()
        text_stim.draw()
        if valid_gaze_pos:
            if EYE_TRACKER:
                gaze_dot.draw()
        
        # Display updated stim on screen
        flip_time = win.flip()
            
        # Check joystick for trigger presses
        if JOYSTICK and frame_num%5==0:
            pygame.event.poll() # Look for joystick events
            button = joystick.get_button( 7 ) # 'Z'-trigger button
        
        # Check keyboard for button presses
        keys = keyboard.getPresses()

        # Check any new keyboard char events for a space key
        # If one is found, set the trial end variable
        if ' ' in keyboard.getPresses() or mov.status == visual.FINISHED or button:
            run_trial = False
            
        # Check any new keyboard char events for a 'q' key
        # If one is found, set the trial break variable
        if 'q' in keys:
            break_trial = True
            break
    
    # Current Trial is Done
    # If trial break variable is set, break trial
    if break_trial:
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
        
    # Pause for ISI +/- random jitter duration
    time.sleep(ISI + jitter_times[trial_num])
    
    # Log ISI end time for header
    ISI_END[trial_num] = core.getTime()

# All Trials are done

# Create header array from lists
head = zip(np.arange(TRIAL_COUNT)+1,new_order+1,videolist,SCR_OPEN,SCR_CLOSE,ISI_END)

# Write header array to csv file
with open(headerpath + header_nm + '.csv', 'wb') as f:
    writer = csv.writer(f)
    for val in head:
        writer.writerow(val)
        
# Tell user about saved header
print "Header file saved: " + header_nm
        
# End experiment
win.close()
if EYE_TRACKER:
    tracker.setConnectionState(False)
io.quit()
core.quit()