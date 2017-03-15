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

from psychopy import core, visual #, parallel
from psychopy.iohub.client import launchHubServer

# Force psychopy to use particular audio library
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

import glob, time, csv, datetime, wx, xbox, os, cv2 # , subprocess
import numpy as np

# Import custom functions
from buttonDemo import buttonDemo
from plot_beh import plot_beh

# Show credits
def presents( win ):
 
    # Create text object       
    text_str = "Petkov/Howard Labs Present"
    text = visual.TextStim(win, height = 45,
                               wrapWidth = width,
                               alignHoriz='center',
                               text=text_str,
                               antialias=True,
                               font='Impact Label Reversed')
                                                    
    # Animate background (fade-in)
    for i in fade_in[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()
        win.flip()
                
    # Play sound
    if MUSIC:
            guitar_snd.play()
     
    # Pause briefly       
    time.sleep(.2)
    
    # Animate (fade-out)
    for i in fade_out[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()    
        win.flip()
    
    time.sleep(.25)

# Show credits
def presents( win ):
 
    # Create text object       
    text_str = "Petkov/Howard Labs Present"
    text = visual.TextStim(win, height = 45,
                               wrapWidth = width,
                               alignHoriz='center',
                               text=text_str,
                               antialias=True,
                               font='Impact Label Reversed')
                                                    
    # Animate background (fade-in)
    for i in fade_in[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()
        win.flip()
                
    # Play sound
    if MUSIC:
            guitar_snd.play()
     
    # Pause briefly       
    time.sleep(.2)
    
    # Animate (fade-out)
    for i in fade_out[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()    
        win.flip()
    
    time.sleep(.25)

# Start screen function
def start_screen( win ):

    zoom_step = 50
      
    # Get image dimensions for mask
    height,width = start_img._origSize
               
    # Play music
    if MUSIC:
        theme_snd.play() 
    
    # Zoom effect (open)    
    for i in range(1,int(width/2),zoom_step):
        
        # Create mask        
        circle_img = np.ones((height,width), np.uint8)*-1
        cv2.circle(circle_img,(int(width/2),int(height/2)),i,1,thickness=-1)
        start_img.setMask(circle_img)
    
        # Draw the image to window and show on screen
        start_img.draw()
        win.flip()
    
    # Wait on 'Start' button press
    while True:
        # Check devices for button presses
        keys = keyboard.getPresses()
        if joy.Start() or (' ' in keys):
            quit_game = False
            
            # Acknowledge button press with sound
            if MUSIC:
                theme_snd.stop()
                laserSound()
                
            # Zoom effect (close)
            for i in range(int(width/2),1,-zoom_step*2):
                
                # Create mask
                circle_img = np.ones((height,width), np.uint8)*-1
                cv2.circle(circle_img,(int(width/2),int(height/2)),i,1,thickness=-1)
                start_img.setMask(circle_img)
            
                # Draw the image to window and show on screen
                start_img.draw()
                win.flip()
            
            break
        
        elif joy.Back() or ('q' in keys):
            quit_game = True
            
            # Stop music and break
            if MUSIC:
                theme_snd.stop()        
            break
        
    return quit_game
        
# Give subject instructions
def instruct_screen( win ):
    
    instruct_play = True
    
    def start_break():
    # Break if 'start' or 'space' is pressed
        if joy.Start() or (' ' in keyboard.getPresses()):
            instruct_play = False
            if MUSIC:
                laserSound()
        else:
            instruct_play = True
        return instruct_play
                
    # Play music
    if MUSIC:
        mission_snd.play()
    
    start_pos = np.array([0, -height/3])  # [x, y] norm units in this case where TextSTim inherits 'units' from the Window, which has 'norm' as default.
    end_pos = np.array([0, -height/20.0])
    animation_duration = 400  # duration in number of frames
    step_pos = (end_pos - start_pos)/animation_duration
    
    # Create text object                       
    instrFin_text = visual.TextStim(win=win, text="Press Start to continue",
                               pos = [0, -(height/2)+50],
                               height = 45,
                               wrapWidth = width,
                               antialias=True,
                               alignHoriz='center',
                               font='Road Rage')
    
    # Set initial position of instruction-text image
    instr_img.pos = start_pos
    
    # Animate (fade-in)
    for i in fade_in[::6]:
        if (instruct_play):
            back_img.draw()
            instr_img.mask = np.ones((2**10,2**10), np.uint8)*i
            instr_img.draw()
            win.flip()
            
            # Check if 'start' or space bar are pressed
            instruct_play = start_break()
        else:
            break
    
    # Animate (scroll text vertically)
    for i in range(animation_duration):
        if (instruct_play):
            instr_img.pos += step_pos  # Add to existing value
            
            # Draw images to window and show on screen
            back_img.draw()
            instr_img.draw()
            win.flip()
            
            # Check if 'start' or space bar are pressed
            instruct_play = start_break()
        else:
            break
    
    cont_step = -.1
    cont_out = 1.0  
    
    # Instruct user to press 'Start' and wait on button press
    while (instruct_play):
        
        # Oscillate text contrast while we wait
        cont_out = cont_out + cont_step
        if (cont_out<-.9) or (cont_out>.9):
            cont_step *= -1
        instrFin_text.contrast = cont_out

        # Draw everything to the screen and post
        back_img.draw()
        instr_img.draw()
        instrFin_text.draw()
        time.sleep(.01)
        win.flip()
        
        # Break if 'start' or 'space' is pressed
        instruct_play = start_break()

    # Stop music
    if MUSIC:
        mission_snd.stop()
                
def readySet( win ):
            
    # Show "Mission starting in:"
    text_start = visual.TextStim(win=win,
                                 height=28,
                                 pos = [0, height/6],
                                 antialias=True,
                                 text="Mission starting in:")
    
    # Animate (fade-in)
    for i in fade_in[::4]:
        text_start.contrast = i 
        text_start.draw()
        win.flip()
                                 
    for i in range(3,0,-1):
        
        # Play sound
        if MUSIC:   
            beep_snd.play()
        
        # Show count-down        
        text = visual.TextStim(win,
                               height=100,
                               bold=True,
                               antialias=True,
                               text=str(i),
                                font='DS-Digital')
    
        # Animate (fade-out)
        for i in fade_out:
            text.contrast = i 
            text_start.draw()
            text.draw()    
            win.flip()
    
    # Show "Go!"
    text = visual.TextStim(win,
                           height=56,
                           bold=True,
                           antialias=True,
                           text="Go!")
    text.draw()    
    win.flip()

    time.sleep(.25)
    
def segue( win ):
                          
    # Animate background (fade-in)
    for i in fade_in[::4]:
        back_img.mask = np.ones((2**10,2**10), np.uint8)*i
        back_img.draw()
        win.flip()
        
    # Play sound
    if MUSIC:
            morse_snd.play()
            
    # Show message        
    text_str = "Incoming transmissions for {}".format(user_name)
    text = visual.TextStim(win, height = 45,
                               wrapWidth = width,
                               alignHoriz='center',
                               text=text_str,
                               antialias=True,
                               font='Top Secret')
                
    # Post to screen and pause briefly
    back_img.draw()
    text.draw()    
    win.flip()
    time.sleep(.2)
    
    # Animate (fade-out)
    for i in fade_out:
        text.contrast = i
        back_img.draw()
        text.draw()    
        win.flip()
    
    time.sleep(.4)
#    morse_snd.stop()

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

    while time.time()-curr_time < delay:
        if cmd_list[0]():
            resp = 0
        elif cmd_list[1]():
            resp = 1
        elif cmd_list[2]():
            resp = 2
        elif cmd_list[3]():
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
        tyson_snd.play()
    
    text_str = user_name + "'s score:"
    corr_str = "{}%".format(ave_str)
    
    # Create text and image objects
    text = visual.TextStim(win, text=text_str,
                           height=50,
                           alignHoriz='center',
                           wrapWidth = width,
                           antialias=True,
                           pos = [0, height/3])
    score_text = visual.TextStim(win, text=corr_str,
                           height=70,
                           color=barCol,
                           alignHoriz='center',
                           bold=True,
                           wrapWidth = width,
                           antialias=True,
                           pos = [width/6, 0])
    fin_text = visual.TextStim(win, text="Play again? <Press Start>",
                           height=50,
                           alignHoriz='center',
                           wrapWidth = width,
                           pos = [0, -height/2.5],
                           antialias=True,
                           font='Top Secret')  
    
    # Load image of behavioral figure we just created                       
    beh_img = visual.ImageStim(win=win,
                               image = beh_fig_name,
                               units = "pix",
                               pos = [-width/5, 0])
#    beh_img.size *= .75  # scale the image relative to initial size
        
    cont_step = -.1
    cont_out = 1.0 
        
    # Instruct user to press 'Start' and wait on button press
    while break_endscr==False:
        
        # Oscillate text contrast while we wait
        cont_out = cont_out + cont_step
        if (cont_out<-.9) or (cont_out>.9):
            cont_step *= -1
        fin_text.contrast = cont_out

        # Draw everything and post to screen
        back_img.draw()
        beh_img.draw()
        text.draw()
        score_text.draw()
        fin_text.draw()
        win.flip()
        
        # Check devices for button presses
        keys = keyboard.getPresses()
        if joy.Start() or (' ' in keys):       
            # Acknowledge button press with sound
            if MUSIC:
                tyson_snd.stop()
                laserSound()
                
            # Animate
            text.contrast = 1
            for i in np.array(range(100,-100,-4))/100.0:
                text.contrast = i
                beh_img.contrast = i                
                back_img.draw()
                beh_img.draw()
                text.draw()
                win.flip()
                
            quit_game=False
            break_endscr=True
            
            break
        elif joy.Back() or ('q' in keys):
            # Stop music
            if MUSIC:
                tyson_snd.stop()
            quit_game=True
            break_endscr=True
            break
    return quit_game

## Start script - initialize variables

# Initialize boolean to break and end experiment
quit_game=False

# Counter
play_reps=0

# Define path to git repo
main_dir=os.environ['HOME']+"/Desktop/py_stimuli/"

# Define path for figure output
fig_dir=main_dir+"expEyeTrack/beh_figs/"
    
# Find movies matching wildcard search
videopath=main_dir+"JonesStimset/"
videolist=glob.glob(videopath + '*.avi')
#videolist = videolist[0:5]

# Set header path
headerpath=main_dir+"expEyeTrack/headers/"

# Get current screen size (works for single monitor only)
app = wx.App(False)
width, height = wx.GetDisplaySize()
    
# Lateral side of controller to use
SIDE='L'
# Number of trials of each stimulus to run
BLOCK_REPS=1
# Decision cue window (seconds)
DEC_WIN=2
# Inter-stimulus interval (seconds)
ISI=1
# Jitter range (+/-seconds)
JITTER=.1
# Scaling of image (none = 1)
SCALE=1
# Volume of sound effects
SND_VOL=.25

# Boolean for debugging mode
TESTING=0; # 1: yes, 0: no
# Boolean for including control stimuli
CONTROLS=0; # 1: yes, 0: no
# Boolean for presence of tracker
EYE_TRACKER=0; # 1: yes, 0: no
# Boolean to simulate tracker activity with mouse
SIMULATE=1; # 1: yes, 0: no
# Boolean for presence of joystick (N64 only, currently)
JOYSTICK=1; # 1: yes, 0: no1
# Boolean for intro music
MUSIC=1; # 1: yes, 0: no

# Define fades
fade_in = tuple(np.array(range(-100,100,2))/100.0)
fade_out = tuple(np.array(range(100,-100,-2))/100.0)

if MUSIC:
    def laserSound():
        # Acknowledge button press with sound
        laser_snd.play()
        
if JOYSTICK:
    # Initialize joystick device - reload module, if necessary
    try:
        joy = xbox.Joystick()
    except:
        import xbox
        joy = xbox.Joystick()
        
    if SIDE=='R':
        # Create list of functions corresponding to each button used
        cmd_list = [lambda:joy.Y(),
                    lambda:joy.B(),
                    lambda:joy.A(),
                    lambda:joy.X()]
    else:
        # Create list of functions corresponding to each button used
        cmd_list = [lambda:joy.dpadUp(),
                    lambda:joy.dpadRight(),
                    lambda:joy.dpadDown(),
                    lambda:joy.dpadLeft()] 

    
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
PHOTO_POS = tuple(np.floor((SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1]))

# Prompt user for player name
if TESTING==1:
    user_name = "Agent Qwe"
else:
    user_name = "Agent " + raw_input('Enter player\'s name [e.g. Fabio]: ').title()

## Create window
win = visual.Window(SCREEN_SIZE.tolist(),
                    units='pix',
                    fullscr=FLSCRN,
                    allowGUI=False,
                    color=[-1,-1,-1],  
                    winType='pyglet')
                    
# Fill window with loading screen
load_text = visual.TextStim(win=win,
                            text="Loading...",
                               height = 50,
                               wrapWidth = width,
                               antialias=True,
                               alignHoriz='center', 
                               font='Road Rage')

# Animate (fade-in)
for i in fade_in:
    load_text.contrast = i
    load_text.draw()    
    win.flip()
    
# Load sounds (and set volumes)                             
if MUSIC:
    laser_snd = sound.Sound(value = "laser.wav") # For 'start' button press sound
    laser_snd.setVolume(SND_VOL*2)

    theme_snd = sound.Sound(value = "theme.wav") # Start-screen music
    theme_snd.setVolume(SND_VOL)             
    
    tyson_snd = sound.Sound(value = "tyson.wav") # End-screen music
    tyson_snd.setVolume(SND_VOL*2)              
                  
    mission_snd = sound.Sound(value = "mission-briefing.wav") # Instruction-screen music
    mission_snd.setVolume(SND_VOL)
        
    beep_snd = sound.Sound(value="beep.wav")
    beep_snd.setVolume(SND_VOL)       

    morse_snd = sound.Sound(value = "morse.wav")
    morse_snd.setVolume(SND_VOL)
    
    guitar_snd = sound.Sound(value = "guitar.wav")
    guitar_snd.setVolume(SND_VOL)

# Load images (and set scales)
# Instruction-screen background image                           
back_img = visual.ImageStim(win=win,image="stars.jpg",units="pix")
dec_img = visual.ImageStim(win=win,image="decision.png",units="pix")
right_img = visual.ImageStim(win=win,image="right.png",units="pix")
wrong_img = visual.ImageStim(win=win,image="wrong.png",units="pix")
# Image (scaled to 2**10X2**10)                                          
start_img = visual.ImageStim(win=win,image="start_screen_scl.png",units="pix")
instr_img = visual.ImageStim(win=win,image="instructions.png",units="pix")
guitar_img = visual.ImageStim(win=win,image="guitar.png",units="pix")
              
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
#port = parallel.ParallelPort(address=0x0378)
    
if EYE_TRACKER:
    # Run eyetracker calibration
    r = tracker.runSetupProcedure()

while quit_game==False:
    
    # Set header path and file name (according to current time)
    header_nm = 'hdr'+datetime.datetime.now().strftime("%m%d%Y_%H%M")
        
    # Create new stimulus order for entire experiment
    perm_list = [ np.random.permutation(len(videolist)) for i in range(BLOCK_REPS) ]
    new_order = np.concatenate(perm_list)
        
    # Re-order (and grow, if necessary) stimulus list
    videolist = tuple([ videolist[i] for i in new_order ])
    
    # Extract identity numbers from video list
    ident_ind = videolist[0].rfind('/')+len("identity")+1
    
    # Get trajectory (radial v. tangential) from video list    
    TRAJ_LIST = (np.unique([x[ident_ind+1:ident_ind+4] for x in videolist],return_inverse = True)[1])

    # Get position along trajectory (identity level) from video list        
    STEP_LIST = (np.unique([x[ident_ind+5:ident_ind+8] for x in videolist],return_inverse = True)[1])
    
    # ident_ind = videolist[0].find("identity")+len("identity")
    IDENT_LIST = np.unique([x[ident_ind] for x in videolist],return_inverse = True)[1]
    
    # Assign identity # for faces more than 50% along tang. trajectory to opposing identity
    temp1 = IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST==2))] + 1
    temp1[temp1==max(temp1)] = 0
    IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST==2))] = temp1
    IDENT_LIST = (IDENT_LIST)
        
    # Create jitter times (uniformly distributed)
    jitter_times = tuple(np.random.uniform(-JITTER, JITTER, TRIAL_COUNT))
    
    # Pre-allocate timing lists
    SCR_OPEN = [None] * TRIAL_COUNT
    SCR_CLOSE = [None] * TRIAL_COUNT
    ISI_END = [None] * TRIAL_COUNT
    
    # Pre-allocate response list
    RESP = [None] * TRIAL_COUNT
    RESP_TIME = [None] * TRIAL_COUNT
    CORRECT = [None] * TRIAL_COUNT
    CORRECT[0] = 0 # Initialize with zero so the running average works at the beginning  
        
    # Animate load-screen (fade-out)
    for i in fade_out[::2]:
        load_text.contrast = i
        load_text.draw()    
        win.flip()
    
    # Show credits 
    if play_reps==0:
        presents(win)
        
    # Define window objects
    if JOYSTICK:
        
        if play_reps==0:
            # Display start screen and wait for user to press 'Start'
            quit_game = start_screen(win)
        play_reps += 1
        
        if quit_game:
            break

        # Show 'incoming message...' animation
        segue(win)
               
        # Display instruction screen, then wait for user to press 'Start'
        instruct_screen(win)
        
        # Display demonstration of identities and corresponding dpad directions
        buttonDemo(win,joy,keyboard,SIDE)
        
    # Countdown to start
    readySet(win)
    
    # Set up eye-tracker visual objects
    if EYE_TRACKER:
        gaze_ok_region = visual.Circle(win,
                                       radius=200,
                                       units='pix')
        gaze_dot = visual.GratingStim(win,
                                      tex=None,
                                      mask='gauss',
                                      pos=(0, 0),
                                      size=(33, 33),
                                      color='green',
                                      units='pix')
    # Set up feedback bar
    if JOYSTICK:
        prog_bar = visual.Rect(win=win,
                               width=75,
                               height=height,
                               pos=[-(width/2),0],
                               fillColor='grey',
                               lineColor='grey')
     
    # Create photodiode patch               
    photodiode = visual.GratingStim(win,
                                    tex=None,
                                    mask='none',
                                    pos=PHOTO_POS,
                                    size=100)
                                    
        
    ## Launch experiment                                 
    globalClock = core.Clock()  # to track the time since experiment started
    buttonDemo
    
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
            corr_bar = visual.Rect(win=win,
                                   width=75,
                                   height=height,
                                   pos=[-(width/2),0+corr_move], fillColor=barCol, lineColor=barCol)
                                                  
        tr_text = visual.TextStim(win,
                                  text=(str(trial_num+1)),
                                  antialias=True)
        tr_rect = visual.Rect(win,
                              width=tr_text.boundingBox[0],
                              height=tr_text.boundingBox[1])
        tr_text.pos = [(width/2)-tr_text.boundingBox[0],(height/2)-tr_text.boundingBox[1]]     
        tr_rect.pos = tr_text.pos      
                  
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win,
                                videolist[trial_num]) 
        
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
            
            # Check any new keyboard char events for a 'q' key
            # If one is found, set the experiment break boolean
            if joy.Back() or ('q' in keyboard.getPresses()):
                quit_game = True
                break
        
        # Current Trial is Done
        
        # If trial break variable is set, break trial
        if quit_game:
            break
                
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
         
        # Check joystick for button presses
        if JOYSTICK:
            
            # Poll joystick for X seconds
            RESP[trial_num], RESP_TIME[trial_num] = poll_buttons(DEC_WIN)
        
        # Pause for n seconds
        tr_text.draw()
        tr_rect.draw()
        if JOYSTICK:
            prog_bar.draw()
            corr_bar.draw()
#        win.flip(clearBuffer=True)
        time.sleep(ISI + jitter_times[trial_num])
            
        # Log ISI end time for header
        ISI_END[trial_num] = core.getTime()
    
    ## Save log files    
    save_logs()
    
#    ## Save psychometric figs
    plt = plot_beh(STEP_LIST,TRAJ_LIST,CORRECT,rad_only=True,SCORE=average)
    figOut_name = fig_dir + "beh_fig_" + header_nm + ".png"    
    plt.savefig(filename=figOut_name,
                dpi=100, transparent=True)
    plt.close()
    
    # All Trials are done
    quit_game = end_screen( win, figOut_name )
    
## End experiment   
win.close() 
if EYE_TRACKER:
    tracker.setConnectionState(False)
if JOYSTICK:
    joy.close()
io.quit()
core.quit()