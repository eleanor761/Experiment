#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on February 12, 2025, at 20:23
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'experiment'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\flani\\Experiment\\experiment_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('learning_inst_resp') is None:
        # initialise learning_inst_resp
        learning_inst_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='learning_inst_resp',
        )
    if deviceManager.getDevice('trial_resp') is None:
        # initialise trial_resp
        trial_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='trial_resp',
        )
    # create speaker 'correct'
    deviceManager.addDevice(
        deviceName='correct',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=-1
    )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('test_resp') is None:
        # initialise test_resp
        test_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='test_resp',
        )
    if deviceManager.getDevice('test_resp_2') is None:
        # initialise test_resp_2
        test_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='test_resp_2',
        )
    if deviceManager.getDevice('test_resp_3') is None:
        # initialise test_resp_3
        test_resp_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='test_resp_3',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "learning_instruction" ---
    learningInstructions = visual.TextStim(win=win, name='learningInstructions',
        text="In this experiment, you will be learning some new actions and their names.\n\nFor each trial, you will see an action at the top of the screen, and two possible names below it. If the action matches the LEFT name, press 'z' on the keyboard. If the action matches the RIGHT name, press '/' on the keyboard. You will hear a 'bleep' if your answer is correct, and a 'buzz' if your answer is incorrect. \n\nWhen you are ready to start, press 's' on the keyboard.",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    learning_inst_resp = keyboard.Keyboard(deviceName='learning_inst_resp')
    
    # --- Initialize components for Routine "learning_trial" ---
    movie = visual.MovieStim(
        win, name='movie',
        filename='test_stimuli/traimin.mp4', movieLib='ffpyplayer',
        loop=True, volume=1.0, noAudio=True,
        pos=(0, 0.25), size=(0.25, 0.25), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    text_left = visual.TextStim(win=win, name='text_left',
        text="'traimin'",
        font='Arial',
        pos=(-.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_right = visual.TextStim(win=win, name='text_right',
        text="'pablize'",
        font='Arial',
        pos=(.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    trial_resp = keyboard.Keyboard(deviceName='trial_resp')
    correct = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='correct',    name='correct'
    )
    correct.setVolume(1.0)
    
    # --- Initialize components for Routine "testing_instruction" ---
    text = visual.TextStim(win=win, name='text',
        text="Nice job! You have completed the learning section of this experiment. Take a break before the next section if you need.\n\nThis next section is the same as the first, however you will no longer hear any feedback when you answer. Do your best to chose the correct answer each time.\n\nWhen you are ready to start, press 's' on the keyboard.",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "testing_trial" ---
    test_movie = visual.MovieStim(
        win, name='test_movie',
        filename='test_stimuli/traimin_obj.mp4', movieLib='ffpyplayer',
        loop=True, volume=1.0, noAudio=True,
        pos=(0, 0.25), size=(0.25, 0.25), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    left_text = visual.TextStim(win=win, name='left_text',
        text="'barbul'",
        font='Arial',
        pos=(-.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    right_text = visual.TextStim(win=win, name='right_text',
        text="'traimin'",
        font='Arial',
        pos=(.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    test_resp = keyboard.Keyboard(deviceName='test_resp')
    
    # --- Initialize components for Routine "testing_trial_2" ---
    test_movie_2 = visual.MovieStim(
        win, name='test_movie_2',
        filename='test_stimuli/joicate/joicate_obj.mp4', movieLib='ffpyplayer',
        loop=True, volume=1.0, noAudio=True,
        pos=(0, 0.25), size=(0.25, 0.25), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    left_text_2 = visual.TextStim(win=win, name='left_text_2',
        text="'joicate'",
        font='Arial',
        pos=(-.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    right_text_2 = visual.TextStim(win=win, name='right_text_2',
        text="'fremple'",
        font='Arial',
        pos=(.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    test_resp_2 = keyboard.Keyboard(deviceName='test_resp_2')
    
    # --- Initialize components for Routine "testing_trial_3" ---
    test_movie_3 = visual.MovieStim(
        win, name='test_movie_3',
        filename='test_stimuli/joicate/joicate_state.mp4', movieLib='ffpyplayer',
        loop=True, volume=1.0, noAudio=True,
        pos=(0, 0.25), size=(0.25, 0.25), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    left_text_3 = visual.TextStim(win=win, name='left_text_3',
        text="'pablize'",
        font='Arial',
        pos=(-.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    right_text_3 = visual.TextStim(win=win, name='right_text_3',
        text="'joicate'",
        font='Arial',
        pos=(.25, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    test_resp_3 = keyboard.Keyboard(deviceName='test_resp_3')
    
    # --- Initialize components for Routine "thank_you" ---
    thanks = visual.TextStim(win=win, name='thanks',
        text='Thank you for participating!\n\nAdd Survey',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "learning_instruction" ---
    # create an object to store info about Routine learning_instruction
    learning_instruction = data.Routine(
        name='learning_instruction',
        components=[learningInstructions, learning_inst_resp],
    )
    learning_instruction.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for learning_inst_resp
    learning_inst_resp.keys = []
    learning_inst_resp.rt = []
    _learning_inst_resp_allKeys = []
    # store start times for learning_instruction
    learning_instruction.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    learning_instruction.tStart = globalClock.getTime(format='float')
    learning_instruction.status = STARTED
    thisExp.addData('learning_instruction.started', learning_instruction.tStart)
    learning_instruction.maxDuration = None
    # keep track of which components have finished
    learning_instructionComponents = learning_instruction.components
    for thisComponent in learning_instruction.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "learning_instruction" ---
    learning_instruction.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *learningInstructions* updates
        
        # if learningInstructions is starting this frame...
        if learningInstructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            learningInstructions.frameNStart = frameN  # exact frame index
            learningInstructions.tStart = t  # local t and not account for scr refresh
            learningInstructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(learningInstructions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'learningInstructions.started')
            # update status
            learningInstructions.status = STARTED
            learningInstructions.setAutoDraw(True)
        
        # if learningInstructions is active this frame...
        if learningInstructions.status == STARTED:
            # update params
            pass
        
        # if learningInstructions is stopping this frame...
        if learningInstructions.status == STARTED:
            if bool(learning_inst_resp.status==FINISHED):
                # keep track of stop time/frame for later
                learningInstructions.tStop = t  # not accounting for scr refresh
                learningInstructions.tStopRefresh = tThisFlipGlobal  # on global time
                learningInstructions.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'learningInstructions.stopped')
                # update status
                learningInstructions.status = FINISHED
                learningInstructions.setAutoDraw(False)
        
        # *learning_inst_resp* updates
        waitOnFlip = False
        
        # if learning_inst_resp is starting this frame...
        if learning_inst_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            learning_inst_resp.frameNStart = frameN  # exact frame index
            learning_inst_resp.tStart = t  # local t and not account for scr refresh
            learning_inst_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(learning_inst_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'learning_inst_resp.started')
            # update status
            learning_inst_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(learning_inst_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(learning_inst_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if learning_inst_resp.status == STARTED and not waitOnFlip:
            theseKeys = learning_inst_resp.getKeys(keyList=['s'], ignoreKeys=["escape"], waitRelease=False)
            _learning_inst_resp_allKeys.extend(theseKeys)
            if len(_learning_inst_resp_allKeys):
                learning_inst_resp.keys = _learning_inst_resp_allKeys[-1].name  # just the last key pressed
                learning_inst_resp.rt = _learning_inst_resp_allKeys[-1].rt
                learning_inst_resp.duration = _learning_inst_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            learning_instruction.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learning_instruction.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "learning_instruction" ---
    for thisComponent in learning_instruction.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for learning_instruction
    learning_instruction.tStop = globalClock.getTime(format='float')
    learning_instruction.tStopRefresh = tThisFlipGlobal
    thisExp.addData('learning_instruction.stopped', learning_instruction.tStop)
    # check responses
    if learning_inst_resp.keys in ['', [], None]:  # No response was made
        learning_inst_resp.keys = None
    thisExp.addData('learning_inst_resp.keys',learning_inst_resp.keys)
    if learning_inst_resp.keys != None:  # we had a response
        thisExp.addData('learning_inst_resp.rt', learning_inst_resp.rt)
        thisExp.addData('learning_inst_resp.duration', learning_inst_resp.duration)
    thisExp.nextEntry()
    # the Routine "learning_instruction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "learning_trial" ---
    # create an object to store info about Routine learning_trial
    learning_trial = data.Routine(
        name='learning_trial',
        components=[movie, text_left, text_right, trial_resp, correct],
    )
    learning_trial.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for trial_resp
    trial_resp.keys = []
    trial_resp.rt = []
    _trial_resp_allKeys = []
    correct.setSound('test_stimuli/bleep.wav', hamming=True)
    correct.setVolume(1.0, log=False)
    correct.seek(0)
    # store start times for learning_trial
    learning_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    learning_trial.tStart = globalClock.getTime(format='float')
    learning_trial.status = STARTED
    thisExp.addData('learning_trial.started', learning_trial.tStart)
    learning_trial.maxDuration = None
    # keep track of which components have finished
    learning_trialComponents = learning_trial.components
    for thisComponent in learning_trial.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "learning_trial" ---
    learning_trial.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie* updates
        
        # if movie is starting this frame...
        if movie.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie.frameNStart = frameN  # exact frame index
            movie.tStart = t  # local t and not account for scr refresh
            movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'movie.started')
            # update status
            movie.status = STARTED
            movie.setAutoDraw(True)
            movie.play()
        
        # if movie is stopping this frame...
        if movie.status == STARTED:
            if bool(trial_resp.status==FINISHED) or movie.isFinished:
                # keep track of stop time/frame for later
                movie.tStop = t  # not accounting for scr refresh
                movie.tStopRefresh = tThisFlipGlobal  # on global time
                movie.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'movie.stopped')
                # update status
                movie.status = FINISHED
                movie.setAutoDraw(False)
                movie.stop()
        
        # *text_left* updates
        
        # if text_left is starting this frame...
        if text_left.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_left.frameNStart = frameN  # exact frame index
            text_left.tStart = t  # local t and not account for scr refresh
            text_left.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_left, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_left.started')
            # update status
            text_left.status = STARTED
            text_left.setAutoDraw(True)
        
        # if text_left is active this frame...
        if text_left.status == STARTED:
            # update params
            pass
        
        # if text_left is stopping this frame...
        if text_left.status == STARTED:
            if bool(correct.status==FINISHED):
                # keep track of stop time/frame for later
                text_left.tStop = t  # not accounting for scr refresh
                text_left.tStopRefresh = tThisFlipGlobal  # on global time
                text_left.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_left.stopped')
                # update status
                text_left.status = FINISHED
                text_left.setAutoDraw(False)
        
        # *text_right* updates
        
        # if text_right is starting this frame...
        if text_right.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_right.frameNStart = frameN  # exact frame index
            text_right.tStart = t  # local t and not account for scr refresh
            text_right.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_right, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_right.started')
            # update status
            text_right.status = STARTED
            text_right.setAutoDraw(True)
        
        # if text_right is active this frame...
        if text_right.status == STARTED:
            # update params
            pass
        
        # if text_right is stopping this frame...
        if text_right.status == STARTED:
            if bool(correct.status==FINISHED):
                # keep track of stop time/frame for later
                text_right.tStop = t  # not accounting for scr refresh
                text_right.tStopRefresh = tThisFlipGlobal  # on global time
                text_right.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_right.stopped')
                # update status
                text_right.status = FINISHED
                text_right.setAutoDraw(False)
        
        # *trial_resp* updates
        waitOnFlip = False
        
        # if trial_resp is starting this frame...
        if trial_resp.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
            # keep track of start time/frame for later
            trial_resp.frameNStart = frameN  # exact frame index
            trial_resp.tStart = t  # local t and not account for scr refresh
            trial_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trial_resp.started')
            # update status
            trial_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_resp.status == STARTED and not waitOnFlip:
            theseKeys = trial_resp.getKeys(keyList=['z', 'slash'], ignoreKeys=["escape"], waitRelease=False)
            _trial_resp_allKeys.extend(theseKeys)
            if len(_trial_resp_allKeys):
                trial_resp.keys = _trial_resp_allKeys[-1].name  # just the last key pressed
                trial_resp.rt = _trial_resp_allKeys[-1].rt
                trial_resp.duration = _trial_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *correct* updates
        
        # if correct is starting this frame...
        if correct.status == NOT_STARTED and trial_resp.status==FINISHED:
            # keep track of start time/frame for later
            correct.frameNStart = frameN  # exact frame index
            correct.tStart = t  # local t and not account for scr refresh
            correct.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('correct.started', tThisFlipGlobal)
            # update status
            correct.status = STARTED
            correct.play(when=win)  # sync with win flip
        
        # if correct is stopping this frame...
        if correct.status == STARTED:
            if bool(False) or correct.isFinished:
                # keep track of stop time/frame for later
                correct.tStop = t  # not accounting for scr refresh
                correct.tStopRefresh = tThisFlipGlobal  # on global time
                correct.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'correct.stopped')
                # update status
                correct.status = FINISHED
                correct.stop()
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[movie, correct]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            learning_trial.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learning_trial.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "learning_trial" ---
    for thisComponent in learning_trial.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for learning_trial
    learning_trial.tStop = globalClock.getTime(format='float')
    learning_trial.tStopRefresh = tThisFlipGlobal
    thisExp.addData('learning_trial.stopped', learning_trial.tStop)
    movie.stop()  # ensure movie has stopped at end of Routine
    # check responses
    if trial_resp.keys in ['', [], None]:  # No response was made
        trial_resp.keys = None
    thisExp.addData('trial_resp.keys',trial_resp.keys)
    if trial_resp.keys != None:  # we had a response
        thisExp.addData('trial_resp.rt', trial_resp.rt)
        thisExp.addData('trial_resp.duration', trial_resp.duration)
    thisExp.nextEntry()
    # the Routine "learning_trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "testing_instruction" ---
    # create an object to store info about Routine testing_instruction
    testing_instruction = data.Routine(
        name='testing_instruction',
        components=[text, key_resp],
    )
    testing_instruction.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for testing_instruction
    testing_instruction.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    testing_instruction.tStart = globalClock.getTime(format='float')
    testing_instruction.status = STARTED
    thisExp.addData('testing_instruction.started', testing_instruction.tStart)
    testing_instruction.maxDuration = None
    # keep track of which components have finished
    testing_instructionComponents = testing_instruction.components
    for thisComponent in testing_instruction.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "testing_instruction" ---
    testing_instruction.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # if text is stopping this frame...
        if text.status == STARTED:
            if bool(key_resp.status==FINISHED):
                # keep track of stop time/frame for later
                text.tStop = t  # not accounting for scr refresh
                text.tStopRefresh = tThisFlipGlobal  # on global time
                text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.stopped')
                # update status
                text.status = FINISHED
                text.setAutoDraw(False)
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['s'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            testing_instruction.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testing_instruction.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "testing_instruction" ---
    for thisComponent in testing_instruction.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for testing_instruction
    testing_instruction.tStop = globalClock.getTime(format='float')
    testing_instruction.tStopRefresh = tThisFlipGlobal
    thisExp.addData('testing_instruction.stopped', testing_instruction.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "testing_instruction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "testing_trial" ---
    # create an object to store info about Routine testing_trial
    testing_trial = data.Routine(
        name='testing_trial',
        components=[test_movie, left_text, right_text, test_resp],
    )
    testing_trial.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for test_resp
    test_resp.keys = []
    test_resp.rt = []
    _test_resp_allKeys = []
    # store start times for testing_trial
    testing_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    testing_trial.tStart = globalClock.getTime(format='float')
    testing_trial.status = STARTED
    thisExp.addData('testing_trial.started', testing_trial.tStart)
    testing_trial.maxDuration = None
    # keep track of which components have finished
    testing_trialComponents = testing_trial.components
    for thisComponent in testing_trial.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "testing_trial" ---
    testing_trial.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_movie* updates
        
        # if test_movie is starting this frame...
        if test_movie.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_movie.frameNStart = frameN  # exact frame index
            test_movie.tStart = t  # local t and not account for scr refresh
            test_movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_movie, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_movie.started')
            # update status
            test_movie.status = STARTED
            test_movie.setAutoDraw(True)
            test_movie.play()
        
        # if test_movie is stopping this frame...
        if test_movie.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > test_resp.status==FINISHED-frameTolerance or test_movie.isFinished:
                # keep track of stop time/frame for later
                test_movie.tStop = t  # not accounting for scr refresh
                test_movie.tStopRefresh = tThisFlipGlobal  # on global time
                test_movie.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_movie.stopped')
                # update status
                test_movie.status = FINISHED
                test_movie.setAutoDraw(False)
                test_movie.stop()
        
        # *left_text* updates
        
        # if left_text is starting this frame...
        if left_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_text.frameNStart = frameN  # exact frame index
            left_text.tStart = t  # local t and not account for scr refresh
            left_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'left_text.started')
            # update status
            left_text.status = STARTED
            left_text.setAutoDraw(True)
        
        # if left_text is active this frame...
        if left_text.status == STARTED:
            # update params
            pass
        
        # if left_text is stopping this frame...
        if left_text.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                left_text.tStop = t  # not accounting for scr refresh
                left_text.tStopRefresh = tThisFlipGlobal  # on global time
                left_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_text.stopped')
                # update status
                left_text.status = FINISHED
                left_text.setAutoDraw(False)
        
        # *right_text* updates
        
        # if right_text is starting this frame...
        if right_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_text.frameNStart = frameN  # exact frame index
            right_text.tStart = t  # local t and not account for scr refresh
            right_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'right_text.started')
            # update status
            right_text.status = STARTED
            right_text.setAutoDraw(True)
        
        # if right_text is active this frame...
        if right_text.status == STARTED:
            # update params
            pass
        
        # if right_text is stopping this frame...
        if right_text.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                right_text.tStop = t  # not accounting for scr refresh
                right_text.tStopRefresh = tThisFlipGlobal  # on global time
                right_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_text.stopped')
                # update status
                right_text.status = FINISHED
                right_text.setAutoDraw(False)
        
        # *test_resp* updates
        waitOnFlip = False
        
        # if test_resp is starting this frame...
        if test_resp.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
            # keep track of start time/frame for later
            test_resp.frameNStart = frameN  # exact frame index
            test_resp.tStart = t  # local t and not account for scr refresh
            test_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_resp.started')
            # update status
            test_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(test_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(test_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if test_resp.status == STARTED and not waitOnFlip:
            theseKeys = test_resp.getKeys(keyList=['z', 'slash'], ignoreKeys=["escape"], waitRelease=False)
            _test_resp_allKeys.extend(theseKeys)
            if len(_test_resp_allKeys):
                test_resp.keys = _test_resp_allKeys[-1].name  # just the last key pressed
                test_resp.rt = _test_resp_allKeys[-1].rt
                test_resp.duration = _test_resp_allKeys[-1].duration
                # was this correct?
                if (test_resp.keys == str("'/'")) or (test_resp.keys == "'/'"):
                    test_resp.corr = 1
                else:
                    test_resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[test_movie]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            testing_trial.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testing_trial.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "testing_trial" ---
    for thisComponent in testing_trial.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for testing_trial
    testing_trial.tStop = globalClock.getTime(format='float')
    testing_trial.tStopRefresh = tThisFlipGlobal
    thisExp.addData('testing_trial.stopped', testing_trial.tStop)
    test_movie.stop()  # ensure movie has stopped at end of Routine
    # check responses
    if test_resp.keys in ['', [], None]:  # No response was made
        test_resp.keys = None
        # was no response the correct answer?!
        if str("'/'").lower() == 'none':
           test_resp.corr = 1;  # correct non-response
        else:
           test_resp.corr = 0;  # failed to respond (incorrectly)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('test_resp.keys',test_resp.keys)
    thisExp.addData('test_resp.corr', test_resp.corr)
    if test_resp.keys != None:  # we had a response
        thisExp.addData('test_resp.rt', test_resp.rt)
        thisExp.addData('test_resp.duration', test_resp.duration)
    thisExp.nextEntry()
    # the Routine "testing_trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "testing_trial_2" ---
    # create an object to store info about Routine testing_trial_2
    testing_trial_2 = data.Routine(
        name='testing_trial_2',
        components=[test_movie_2, left_text_2, right_text_2, test_resp_2],
    )
    testing_trial_2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for test_resp_2
    test_resp_2.keys = []
    test_resp_2.rt = []
    _test_resp_2_allKeys = []
    # store start times for testing_trial_2
    testing_trial_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    testing_trial_2.tStart = globalClock.getTime(format='float')
    testing_trial_2.status = STARTED
    thisExp.addData('testing_trial_2.started', testing_trial_2.tStart)
    testing_trial_2.maxDuration = None
    # keep track of which components have finished
    testing_trial_2Components = testing_trial_2.components
    for thisComponent in testing_trial_2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "testing_trial_2" ---
    testing_trial_2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_movie_2* updates
        
        # if test_movie_2 is starting this frame...
        if test_movie_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_movie_2.frameNStart = frameN  # exact frame index
            test_movie_2.tStart = t  # local t and not account for scr refresh
            test_movie_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_movie_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_movie_2.started')
            # update status
            test_movie_2.status = STARTED
            test_movie_2.setAutoDraw(True)
            test_movie_2.play()
        
        # if test_movie_2 is stopping this frame...
        if test_movie_2.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > test_resp.status==FINISHED-frameTolerance or test_movie_2.isFinished:
                # keep track of stop time/frame for later
                test_movie_2.tStop = t  # not accounting for scr refresh
                test_movie_2.tStopRefresh = tThisFlipGlobal  # on global time
                test_movie_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_movie_2.stopped')
                # update status
                test_movie_2.status = FINISHED
                test_movie_2.setAutoDraw(False)
                test_movie_2.stop()
        
        # *left_text_2* updates
        
        # if left_text_2 is starting this frame...
        if left_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_text_2.frameNStart = frameN  # exact frame index
            left_text_2.tStart = t  # local t and not account for scr refresh
            left_text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'left_text_2.started')
            # update status
            left_text_2.status = STARTED
            left_text_2.setAutoDraw(True)
        
        # if left_text_2 is active this frame...
        if left_text_2.status == STARTED:
            # update params
            pass
        
        # if left_text_2 is stopping this frame...
        if left_text_2.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                left_text_2.tStop = t  # not accounting for scr refresh
                left_text_2.tStopRefresh = tThisFlipGlobal  # on global time
                left_text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_text_2.stopped')
                # update status
                left_text_2.status = FINISHED
                left_text_2.setAutoDraw(False)
        
        # *right_text_2* updates
        
        # if right_text_2 is starting this frame...
        if right_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_text_2.frameNStart = frameN  # exact frame index
            right_text_2.tStart = t  # local t and not account for scr refresh
            right_text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'right_text_2.started')
            # update status
            right_text_2.status = STARTED
            right_text_2.setAutoDraw(True)
        
        # if right_text_2 is active this frame...
        if right_text_2.status == STARTED:
            # update params
            pass
        
        # if right_text_2 is stopping this frame...
        if right_text_2.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                right_text_2.tStop = t  # not accounting for scr refresh
                right_text_2.tStopRefresh = tThisFlipGlobal  # on global time
                right_text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_text_2.stopped')
                # update status
                right_text_2.status = FINISHED
                right_text_2.setAutoDraw(False)
        
        # *test_resp_2* updates
        waitOnFlip = False
        
        # if test_resp_2 is starting this frame...
        if test_resp_2.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
            # keep track of start time/frame for later
            test_resp_2.frameNStart = frameN  # exact frame index
            test_resp_2.tStart = t  # local t and not account for scr refresh
            test_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_resp_2.started')
            # update status
            test_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(test_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(test_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if test_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = test_resp_2.getKeys(keyList=['z', 'slash'], ignoreKeys=["escape"], waitRelease=False)
            _test_resp_2_allKeys.extend(theseKeys)
            if len(_test_resp_2_allKeys):
                test_resp_2.keys = _test_resp_2_allKeys[-1].name  # just the last key pressed
                test_resp_2.rt = _test_resp_2_allKeys[-1].rt
                test_resp_2.duration = _test_resp_2_allKeys[-1].duration
                # was this correct?
                if (test_resp_2.keys == str("'/'")) or (test_resp_2.keys == "'/'"):
                    test_resp_2.corr = 1
                else:
                    test_resp_2.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[test_movie_2]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            testing_trial_2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testing_trial_2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "testing_trial_2" ---
    for thisComponent in testing_trial_2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for testing_trial_2
    testing_trial_2.tStop = globalClock.getTime(format='float')
    testing_trial_2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('testing_trial_2.stopped', testing_trial_2.tStop)
    test_movie_2.stop()  # ensure movie has stopped at end of Routine
    # check responses
    if test_resp_2.keys in ['', [], None]:  # No response was made
        test_resp_2.keys = None
        # was no response the correct answer?!
        if str("'/'").lower() == 'none':
           test_resp_2.corr = 1;  # correct non-response
        else:
           test_resp_2.corr = 0;  # failed to respond (incorrectly)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('test_resp_2.keys',test_resp_2.keys)
    thisExp.addData('test_resp_2.corr', test_resp_2.corr)
    if test_resp_2.keys != None:  # we had a response
        thisExp.addData('test_resp_2.rt', test_resp_2.rt)
        thisExp.addData('test_resp_2.duration', test_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "testing_trial_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "testing_trial_3" ---
    # create an object to store info about Routine testing_trial_3
    testing_trial_3 = data.Routine(
        name='testing_trial_3',
        components=[test_movie_3, left_text_3, right_text_3, test_resp_3],
    )
    testing_trial_3.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for test_resp_3
    test_resp_3.keys = []
    test_resp_3.rt = []
    _test_resp_3_allKeys = []
    # store start times for testing_trial_3
    testing_trial_3.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    testing_trial_3.tStart = globalClock.getTime(format='float')
    testing_trial_3.status = STARTED
    thisExp.addData('testing_trial_3.started', testing_trial_3.tStart)
    testing_trial_3.maxDuration = None
    # keep track of which components have finished
    testing_trial_3Components = testing_trial_3.components
    for thisComponent in testing_trial_3.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "testing_trial_3" ---
    testing_trial_3.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *test_movie_3* updates
        
        # if test_movie_3 is starting this frame...
        if test_movie_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            test_movie_3.frameNStart = frameN  # exact frame index
            test_movie_3.tStart = t  # local t and not account for scr refresh
            test_movie_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_movie_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_movie_3.started')
            # update status
            test_movie_3.status = STARTED
            test_movie_3.setAutoDraw(True)
            test_movie_3.play()
        
        # if test_movie_3 is stopping this frame...
        if test_movie_3.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > test_resp.status==FINISHED-frameTolerance or test_movie_3.isFinished:
                # keep track of stop time/frame for later
                test_movie_3.tStop = t  # not accounting for scr refresh
                test_movie_3.tStopRefresh = tThisFlipGlobal  # on global time
                test_movie_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'test_movie_3.stopped')
                # update status
                test_movie_3.status = FINISHED
                test_movie_3.setAutoDraw(False)
                test_movie_3.stop()
        
        # *left_text_3* updates
        
        # if left_text_3 is starting this frame...
        if left_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            left_text_3.frameNStart = frameN  # exact frame index
            left_text_3.tStart = t  # local t and not account for scr refresh
            left_text_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(left_text_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'left_text_3.started')
            # update status
            left_text_3.status = STARTED
            left_text_3.setAutoDraw(True)
        
        # if left_text_3 is active this frame...
        if left_text_3.status == STARTED:
            # update params
            pass
        
        # if left_text_3 is stopping this frame...
        if left_text_3.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                left_text_3.tStop = t  # not accounting for scr refresh
                left_text_3.tStopRefresh = tThisFlipGlobal  # on global time
                left_text_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_text_3.stopped')
                # update status
                left_text_3.status = FINISHED
                left_text_3.setAutoDraw(False)
        
        # *right_text_3* updates
        
        # if right_text_3 is starting this frame...
        if right_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            right_text_3.frameNStart = frameN  # exact frame index
            right_text_3.tStart = t  # local t and not account for scr refresh
            right_text_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(right_text_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'right_text_3.started')
            # update status
            right_text_3.status = STARTED
            right_text_3.setAutoDraw(True)
        
        # if right_text_3 is active this frame...
        if right_text_3.status == STARTED:
            # update params
            pass
        
        # if right_text_3 is stopping this frame...
        if right_text_3.status == STARTED:
            if bool(test_resp.status==FINISHED):
                # keep track of stop time/frame for later
                right_text_3.tStop = t  # not accounting for scr refresh
                right_text_3.tStopRefresh = tThisFlipGlobal  # on global time
                right_text_3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_text_3.stopped')
                # update status
                right_text_3.status = FINISHED
                right_text_3.setAutoDraw(False)
        
        # *test_resp_3* updates
        waitOnFlip = False
        
        # if test_resp_3 is starting this frame...
        if test_resp_3.status == NOT_STARTED and tThisFlip >= 5-frameTolerance:
            # keep track of start time/frame for later
            test_resp_3.frameNStart = frameN  # exact frame index
            test_resp_3.tStart = t  # local t and not account for scr refresh
            test_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(test_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'test_resp_3.started')
            # update status
            test_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(test_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(test_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if test_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = test_resp_3.getKeys(keyList=['z', 'slash'], ignoreKeys=["escape"], waitRelease=False)
            _test_resp_3_allKeys.extend(theseKeys)
            if len(_test_resp_3_allKeys):
                test_resp_3.keys = _test_resp_3_allKeys[-1].name  # just the last key pressed
                test_resp_3.rt = _test_resp_3_allKeys[-1].rt
                test_resp_3.duration = _test_resp_3_allKeys[-1].duration
                # was this correct?
                if (test_resp_3.keys == str("'/'")) or (test_resp_3.keys == "'/'"):
                    test_resp_3.corr = 1
                else:
                    test_resp_3.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[test_movie_3]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            testing_trial_3.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in testing_trial_3.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "testing_trial_3" ---
    for thisComponent in testing_trial_3.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for testing_trial_3
    testing_trial_3.tStop = globalClock.getTime(format='float')
    testing_trial_3.tStopRefresh = tThisFlipGlobal
    thisExp.addData('testing_trial_3.stopped', testing_trial_3.tStop)
    test_movie_3.stop()  # ensure movie has stopped at end of Routine
    # check responses
    if test_resp_3.keys in ['', [], None]:  # No response was made
        test_resp_3.keys = None
        # was no response the correct answer?!
        if str("'/'").lower() == 'none':
           test_resp_3.corr = 1;  # correct non-response
        else:
           test_resp_3.corr = 0;  # failed to respond (incorrectly)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('test_resp_3.keys',test_resp_3.keys)
    thisExp.addData('test_resp_3.corr', test_resp_3.corr)
    if test_resp_3.keys != None:  # we had a response
        thisExp.addData('test_resp_3.rt', test_resp_3.rt)
        thisExp.addData('test_resp_3.duration', test_resp_3.duration)
    thisExp.nextEntry()
    # the Routine "testing_trial_3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "thank_you" ---
    # create an object to store info about Routine thank_you
    thank_you = data.Routine(
        name='thank_you',
        components=[thanks],
    )
    thank_you.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for thank_you
    thank_you.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    thank_you.tStart = globalClock.getTime(format='float')
    thank_you.status = STARTED
    thisExp.addData('thank_you.started', thank_you.tStart)
    thank_you.maxDuration = None
    # keep track of which components have finished
    thank_youComponents = thank_you.components
    for thisComponent in thank_you.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "thank_you" ---
    thank_you.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *thanks* updates
        
        # if thanks is starting this frame...
        if thanks.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            thanks.frameNStart = frameN  # exact frame index
            thanks.tStart = t  # local t and not account for scr refresh
            thanks.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(thanks, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'thanks.started')
            # update status
            thanks.status = STARTED
            thanks.setAutoDraw(True)
        
        # if thanks is active this frame...
        if thanks.status == STARTED:
            # update params
            pass
        
        # if thanks is stopping this frame...
        if thanks.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > thanks.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                thanks.tStop = t  # not accounting for scr refresh
                thanks.tStopRefresh = tThisFlipGlobal  # on global time
                thanks.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'thanks.stopped')
                # update status
                thanks.status = FINISHED
                thanks.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            thank_you.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in thank_you.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "thank_you" ---
    for thisComponent in thank_you.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for thank_you
    thank_you.tStop = globalClock.getTime(format='float')
    thank_you.tStopRefresh = tThisFlipGlobal
    thisExp.addData('thank_you.stopped', thank_you.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if thank_you.maxDurationReached:
        routineTimer.addTime(-thank_you.maxDuration)
    elif thank_you.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
