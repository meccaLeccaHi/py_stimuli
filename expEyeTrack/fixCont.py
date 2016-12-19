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

import time, glob

# Find movies matching wildcard search
videopath = '/home/adam/Desktop/virtBox_share/JonesStimset/identity1/'
videolist = glob.glob(videopath + '*_audVid.avi')

# Number of trials of each stimulus to run
BLOCK_REPS = 1
TRIAL_COUNT = len(videolist) * BLOCK_REPS

iohub_tracker_class_path = 'eyetracker.hw.sr_research.eyelink.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
#eyetracker_config['model_name'] = 'EYELINK 1000 DESKTOP'
eyetracker_config['simulation_mode'] = True
eyetracker_config['runtime_settings'] = dict(sampling_rate=1000,
                                             track_eyes='RIGHT')

# Since no experiment or session code is given, no iohub hdf5 file
# will be saved, but device events are still available at runtime.
io = launchHubServer(**{iohub_tracker_class_path: eyetracker_config})

# Get some iohub devices for future access.
keyboard = io.devices.keyboard
display = io.devices.display
tracker = io.devices.tracker

# run eyetracker calibration
r = tracker.runSetupProcedure()
win = visual.Window(display.getPixelResolution(),
                    units='pix',
                    fullscr=True,
                    allowGUI=False,
                    color='black'
                    )

gaze_ok_region = visual.Circle(win, radius=200, units='pix')

gaze_dot = visual.GratingStim(win, tex=None, mask='gauss', pos=(0, 0),
                              size=(66, 66), color='green', units='pix')
                              
fixation = visual.GratingStim(win, tex=None, mask='circle', sf=0, size=0.03,
                              name='fixation', autoLog=False)
                              
photodiode = visual.GratingStim(win, tex=None, mask='none', sf=0, size=0.2,
                                name='photodiode', autoLog=False, pos=(1,-1))

text_stim_str = 'Eye Position: %.2f, %.2f. In Region: %s\n'
text_stim_str += 'Press space key to start next trial.'
missing_gpos_str = 'Eye Position: MISSING. In Region: No\n'
missing_gpos_str += 'Press space key to start next trial.'
text_stim = visual.TextStim(win, text=text_stim_str,
                            pos=[0, int((-win.size[1]/2)*0.8)], height=24,
                                 color='white',
                                 alignHoriz='center',
                                 alignVert='center', 
                                 wrapWidth=win.size[0] * .9)
# Run blocks.....
for block in range(BLOCK_REPS):
                    
    # Run Trials.....
    for vidPath in videolist:
    
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win, vidPath, size=(366, 332),fps=30,
                                flipVert=False, flipHoriz=False, loop=False) 
                                
        io.clearEvents()
        tracker.setRecordingState(True)
        run_trial = True
        tstart_time = core.getTime()
        
        while run_trial is True:
            
            if mov.status != visual.FINISHED:
                
                # Get the latest gaze position in dispolay coord space..
                gpos = tracker.getLastGazePosition()
        
                # Update stim based on gaze position
                valid_gaze_pos = isinstance(gpos, (tuple, list))
                gaze_in_region = valid_gaze_pos and gaze_ok_region.contains(gpos)
                if valid_gaze_pos:
                    # If we have a gaze position from the tracker, update gc stim
                    # and text stim.
                    if gaze_in_region:
                        gaze_in_region = 'Yes'
                        mov.draw()
                        fixation.draw()
                        photodiode.draw()
                    else:
                        gaze_in_region = 'No'
                        mov.status = visual.FINISHED
                        
                    text_stim.text = text_stim_str % (gpos[0], gpos[1], gaze_in_region)
        
                    gaze_dot.setPos(gpos)
                else:
                    # Otherwise just update text stim
                    text_stim.text = missing_gpos_str
        
                # Redraw stim
                gaze_ok_region.draw()
                text_stim.draw()
                if valid_gaze_pos:
                    gaze_dot.draw()
        
                # Display updated stim on screen.
                flip_time = win.flip()
        
                # Check any new keyboard char events for a space key.
                # If one is found, set the trial end variable.
                #
                if ' ' in keyboard.getPresses() or mov.status == visual.FINISHED:
                    run_trial = False
    
        # Current Trial is Done
        # Stop eye data recording
        tracker.setRecordingState(False)

# All Trials are done
# End experiment
win.close()
tracker.setConnectionState(False)
io.quit()
core.quit()
