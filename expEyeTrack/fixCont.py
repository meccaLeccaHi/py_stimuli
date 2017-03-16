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

from constants import SIDE,BLOCK_REPS,DEC_WIN,ISI,JITTER,SND_VOL,\
TESTING,CONTROLS,EYE_TRACKER,SIM_TRACKER,JOYSTICK,MUSIC,DISPSIZE,\
MAINDIR,STIMDIR,FADEIN,FADEOUT # DISPTYPE,SCALE

# Force psychopy to use particular audio library
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import core, visual, sound #, parallel

from psychopy.iohub.client import launchHubServer

import glob, time, csv, datetime, xbox, os, cv2
import numpy as np

# Import custom functions
from buttonDemo import buttonDemo
from plot_beh import plot_beh

def presents( win ):
    """ Shows credits 
    Arguments: win -- Psychopy window
    Usage: presents( win )
    """
    
    # Create text object       
    text_str = "Petkov/Howard Labs Present"
    text = visual.TextStim(win, height = 55,
                               wrapWidth = width,
                               alignHoriz='center',
                               text=text_str,
                               antialias=True,
                               font='Impact Label Reversed')
                                                    
    # Animate background (fade-in)
    for i in FADEIN[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()
        win.flip()
                
    # Play sound
    if MUSIC:
            guitar_snd.play()
     
    # Pause briefly       
    time.sleep(.5)
    
    # Animate (fade-out)
    for i in FADEOUT[::4]:
        guitar_img.mask = np.ones((2**10,2**10), np.uint8)*i
        guitar_img.draw()
        text.contrast = i
        text.draw()    
        win.flip()
    
    time.sleep(.25)

def start_screen( win ):
    """ Shows start-screen, then waits on 'start' button press 
    Arguments: win -- Psychopy window
    Returns: 'quit_game' boolean
    Usage: start_screen( win )
    """
    
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
        
    print('zoom completed\n')
    
    # Wait on 'Start' button press
    while True:
        # Check devices for button presses
        keys = keyboard.getPresses(clear=True)
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
            
            print('quit on back \n')

            quit_game = True
            
            # Stop music and break
            if MUSIC:
                theme_snd.stop()        
            break
        
    return quit_game
        
def instruct_screen( win ):
    """ Give subject instructions via text, then waits on 'start' button press 
    Arguments: win -- Psychopy window
    Usage: instruct_screen( win )
    """
    
    instruct_play = True
    
    def start_break():
        """ Break if 'start' or 'space' is pressed
        Usage: start_break()
        """
    
        if joy.Start() or (' ' in keyboard.getPresses(clear=True)):
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
    for i in FADEIN[::6]:
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
    """ Show "Mission starting in:"
    Arguments: win -- Psychopy window
    Usage: readySet( win )
    """
            
    # Show "Mission starting in:"
    text_start = visual.TextStim(win=win,
                                 height=28,
                                 pos = [0, height/6],
                                 antialias=True,
                                 text="Mission starting in:")
    
    # Animate (fade-in)
    for i in FADEIN[::4]:
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
        for i in FADEOUT:
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
    """ Shows 'Incoming transmission...' animation
    Arguments: win -- Psychopy window
    Usage: segue( win )
    """
                     
    # Animate background (fade-in)
    for i in FADEIN[::4]:
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
    for i in FADEOUT:
        text.contrast = i
        back_img.draw()
        text.draw()    
        win.flip()
    
    time.sleep(.4)
#    morse_snd.stop()

# Joystick response function
def poll_buttons( delay ):
    """ Waits on joystick response and waits
    Arguments: delay -- How long to wait (in seconds)
    Returns (in order): response (which button was pressed, if any)
                        response time (when that button was pressed)
    Usage: poll_buttons( delay )
    """ 
    
    curr_time = time.time()
    resp = None
    resp_time = None
    
    # Draw decision cue in window and post to screen
    dec_img.draw()
    tr_text.draw()
    tr_rect.draw()
    prog_bar.draw()
    corr_bar.draw()
    win.flip()

    while time.time()-curr_time < delay:
        
        # Loop through response options and return index of non-zero value
        for index, cmd in enumerate(cmd_list):
            if cmd():
                resp = index
                
                # Get the latency of response
                resp_time = time.time()-curr_time
            
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
                
                # Pause until delay time has passed
                time.sleep(delay-resp_time)
                break
    
    return resp, resp_time

def save_logs():
    """ Saves log file to csv .txt file    
    Usage: save_logs()
    """ 
    
    # Create header array from lists
    head = zip(np.arange(TRIAL_COUNT)+1,new_order+1,videolist,SCR_OPEN,SCR_CLOSE,ISI_END,IDENT_LIST,RESP,RESP_TIME,CORRECT,TRAJ_LIST,STEP_LIST)

    # Write header array to csv file
    with open(headerpath + header_nm + '.csv', 'wb') as f:
        writer = csv.writer(f)
        for val in head:
            writer.writerow(val)
        
    # Tell user about saved header
    print "Header file saved: " + header_nm
    
def end_screen( win, beh_fig_name ):
    """ Gives subject feedback at end of each trial
    Arguments: win -- Psychopy window
               beh_fig_name -- File-name for behavioral figure saving
    Returns: 'quit_game' boolean
    Usage: end_screen( win, beh_fig_name )
    """ 
    
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
        keys = keyboard.getPresses(clear=True)
        if joy.Start() or (' ' in keys):       
            # Acknowledge button press with sound
            if MUSIC:
                tyson_snd.stop()
                yes_snd.play()
                
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

# Define path for figure output
fig_dir=MAINDIR+"expEyeTrack/beh_figs/"
    
# Find movies matching wildcard search
videolist=glob.glob(STIMDIR + '*.avi')

# Set header path
headerpath=MAINDIR+"expEyeTrack/headers/"

# Get current screen size
width, height = DISPSIZE

# Prompt user for player name
if TESTING==1:
    user_name = "Agent Qwe"
else:
    user_name = "Agent " + raw_input('Enter player\'s name [e.g. Fabio]: ').title()

if MUSIC:
    def laserSound():
        # Acknowledge button press with sound
        laser_snd.play()

## Initialize devices    
if EYE_TRACKER:
    # Set up eye-tracker configuration dict
    iohub_tracker_class_path = 'eyetracker.hw.sr_research.eyelink.EyeTracker'
    eyetracker_config = dict()
    eyetracker_config['name'] = 'tracker'
    eyetracker_config['simulation_mode'] = (SIM_TRACKER==1)
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

# Set parallel port address
#port = parallel.ParallelPort(address=0x0378)

# Initialize joystick device - reload module, if necessary
try:
    joy = xbox.Joystick()
except:
    import xbox
    joy = xbox.Joystick()

# Create list of functions corresponding to each button used        
if JOYSTICK:
    if SIDE=='R':
        cmd_list = [lambda:joy.Y(),
                    lambda:joy.B(),
                    lambda:joy.A(),
                    lambda:joy.X()]
    else:
        cmd_list = [lambda:joy.dpadUp(),
                    lambda:joy.dpadRight(),
                    lambda:joy.dpadDown(),
                    lambda:joy.dpadLeft()] 
#else:
#    cmd_list = [lambda:int('up' in keyboard.getPresses(clear=True)),
#                lambda:int('right' in keyboard.getPresses(clear=True)),
#                lambda:int('down' in keyboard.getPresses(clear=True)),
#                lambda:int('left' in keyboard.getPresses(clear=True))] 
    
# Include/remove noise controls
if CONTROLS==0:
    videolist = [x for x in videolist if not 'noisy' in x]
    
# Total trial count for experiment
TRIAL_COUNT = len(videolist) * BLOCK_REPS

# Set screen parameters for testing (must be in integer values)
if TESTING:
    FLSCRN = False
    SCREEN_SIZE = np.floor([(x/1.5) for x in np.array(DISPSIZE)])
else:
    FLSCRN = True
    SCREEN_SIZE = np.array(DISPSIZE)

# Set up photodiode
PHOTO_SIZE = 50
# Pixels must be integers
PHOTO_POS = tuple(np.floor((SCREEN_SIZE - PHOTO_SIZE)/2 * [1, -1]))

## Create window
win = visual.Window(tuple(SCREEN_SIZE),
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
for i in FADEIN:
    load_text.contrast = i
    load_text.draw()    
    win.flip()
    
# Load sounds (and set volumes)                             
if MUSIC:
    os.chdir('sounds')
    
    laser_snd = sound.Sound(value = "laser.wav") # For 'start' button press sound
    laser_snd.setVolume(SND_VOL*2)

    yes_snd = sound.Sound(value = "yes.wav") # 'Yes' sound effect
    yes_snd.setVolume(SND_VOL*2)    
    
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
    
# Load images (and set scales) -- should be updated to list comprehension in future updates
os.chdir('../images')                         
back_img = visual.ImageStim(win=win,image="stars.jpg",units="pix") # Instruction-screen background image  
dec_img = visual.ImageStim(win=win,image="decision.png",units="pix")
right_img = visual.ImageStim(win=win,image="right.png",units="pix")
wrong_img = visual.ImageStim(win=win,image="wrong.png",units="pix")
start_img = visual.ImageStim(win=win,image="start_screen_scl.png",units="pix") # Image (scaled to 2**10X2**10)                                          
instr_img = visual.ImageStim(win=win,image="instructions.png",units="pix")
guitar_img = visual.ImageStim(win=win,image="guitar.png",units="pix")
os.chdir('..')  # Return to original parent directory                       

# Main game loop              
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
    
    IDENT_LIST = np.unique([x[ident_ind] for x in videolist],return_inverse = True)[1]
    
    # Assign identity # for faces more than 50% along tang. trajectory to opposing identity
    temp1 = IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST==2))] + 1
    temp1[temp1==max(temp1)] = 0
    IDENT_LIST[np.where((TRAJ_LIST==2)&(STEP_LIST==2))] = temp1
    IDENT_LIST = (IDENT_LIST)
        
    # Create jitter times (uniformly distributed)
    JIT_TIME = tuple(np.random.uniform(-JITTER, JITTER, TRIAL_COUNT))
    
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
    for i in FADEOUT[::2]:
        load_text.contrast = i
        load_text.draw()    
        win.flip()
        
    if EYE_TRACKER:
        # Run eyetracker calibration
        r = tracker.runSetupProcedure()
    
    # Show credits 
    if play_reps==0:
        presents(win)
        
    # Define window objects
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
    
    if JOYSTICK:
        # Display demonstration of identities and corresponding dpad directions
        buttonDemo(win,joy,keyboard,cmd_list)
        
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
    
    # Run Trials.....
    for trial_num in range(TRIAL_COUNT):
        
        # Get current average percent correct
        average = int(np.mean([x for x in CORRECT if x is not None])*100)   
        ave_str = str(average)
        
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
        
        # Create trial counter text object                                      
        tr_text = visual.TextStim(win,
                                  text=(str(trial_num+1)),
                                  antialias=True)
        tr_text.pos = [(width/2)-tr_text.boundingBox[0],(height/2)-tr_text.boundingBox[1]]     
                                  
        # Create bounding box object for trial counter border
        tr_rect = visual.Rect(win,
                              width=tr_text.boundingBox[0],
                              height=tr_text.boundingBox[1])
        tr_rect.pos = tr_text.pos      
                  
        # Create movie stim by loading movie from list
        mov = visual.MovieStim3(win,videolist[trial_num]) 
        
#        io.clearEvents()
        if EYE_TRACKER:
            tracker.setRecordingState(True)
        
        # Add timing of movie opening to header
        SCR_OPEN[trial_num] = core.getTime()
            
        # Start the movie stim by preparing it to play
        mov.play()
            
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
                    mov.draw()
                    
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
            prog_bar.draw()
            corr_bar.draw()
            
            if valid_gaze_pos:
                if EYE_TRACKER:
                    gaze_dot.draw()
            
            # Display updated stim on screen
            flip_time = win.flip()
            
            # Pause or quit, if prompted
            # Check any new keyboard char events
            keys = keyboard.getPresses(clear=True)
            # Check for 'start' or 'space' button presses
            if joy.Start() or (' ' in keys):
                mov.pause() # Pause movie
                
                while True:
                    # Check for 'start' or 'space' button presses
                    if joy.Start() or (' ' in keyboard.getPresses(clear=True)):
                        mov.play() # Resume movie
            # Check for 'back' or 'q' button presses            
            elif joy.Back() or ('q' in keys):
                # Quit game
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
        prog_bar.draw()
        corr_bar.draw()
        
        # Display updated stim on screen
        flip_time = win.flip(clearBuffer=True)
        
        # Log movie end time for header
        SCR_CLOSE[trial_num] = core.getTime()
            
        if EYE_TRACKER:
            # Stop eye data recording
            tracker.setRecordingState(False)
         
        if JOYSTICK:
            # Poll joystick for X seconds
            RESP[trial_num], RESP_TIME[trial_num] = poll_buttons(DEC_WIN)
        else:
            time.sleep(DEC_WIN)
        
        # Pause for x seconds
        tr_text.draw()
        tr_rect.draw()
        prog_bar.draw()
        corr_bar.draw()
        time.sleep(ISI + JIT_TIME[trial_num])
            
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