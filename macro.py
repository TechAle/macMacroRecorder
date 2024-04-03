import random as rd
import threading
import time

import macmouse
from pynput.keyboard import Listener
from pynput.mouse import Controller

mouse = Controller()

macroActive = False

leftWait = 80 / 1000
rightWait = 80 / 1000
leftRightWait = 80 / 1000
rightLeftWait = 80 / 1000
random = 15
currentDone = -1
button = '+'
slowStart = 30

decaySlowStart = 3
addTime = 0


def randomNumber():
    return rd.randint(0, random) / 1000


def buttonLeft():
    if not macroActive:
        return -1
    macmouse.click(button="left")
    global currentDone
    if currentDone == 0:  # Before clicked left
        time.sleep(leftWait + randomNumber() + slowStart / 1000)
    elif currentDone == 1:
        time.sleep(rightLeftWait + randomNumber() + slowStart / 1000)
    currentDone = 0


def buttonRight():
    if not macroActive:
        return -1
    x, y = mouse.position
    mouse.position = (x, y)
    macmouse.click(button="right")
    global currentDone
    if currentDone == 0:  # Before clicked left
        time.sleep(leftRightWait + randomNumber() + slowStart / 1000)
    elif currentDone == 1:
        time.sleep(rightWait + randomNumber() + slowStart / 1000)
    currentDone = 1


def rightLeftLeft():
    buttonRight()
    buttonLeft()
    buttonLeft()


def tpSpell():
    buttonRight()
    buttonRight()
    buttonRight()


def rightLeftRight():
    buttonRight()
    buttonLeft()
    buttonRight()


def rightRightLeft():
    buttonRight()
    buttonRight()
    buttonLeft()


def run():
    global macroActive
    global mouse
    global slowStart
    global addTime
    global decaySlowStart
    addTime = slowStart
    while macroActive:
        rightLeftLeft()
        rightRightLeft()
        addTime -= decaySlowStart
        if addTime <= 0:
            addTime = 0


def onPress(key):
    global macroActive
    try:
        if key.char == button:
            macroActive = not macroActive
            if macroActive:
                threading.Thread(target=run).start()
    except Exception as ignored:
        pass


listener = Listener(on_press=onPress)
listener.start()
listener.join()
