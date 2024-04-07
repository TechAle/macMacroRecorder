import os
import threading
import time

from PyQt5.QtCore import pyqtSignal, QObject
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as ControllerMouse

from variables.MacroState import macroState
from variables.RunnableMacro import runnableMacro


class macroManager():

    def __init__(self, moveMouseTime):
        super().__init__()
        self.scripts = {}
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = ControllerMouse()
        self.isRecording = False
        self.scriptRecording = None
        self.recording = []
        self.lastActionTime = None
        self.lastTimeMoved = None
        self.firstMouseCoords = False
        # Create a locker
        self.locker = threading.Lock()
        self.moveMouseTime = moveMouseTime
        self.scriptRecording = []


    def onToggle(self, script):
        if not self.scripts.__contains__(script):
            return None
        return self.scripts[script].toggle()

    def onCreate(self, script):
        if not self.scripts.keys().__contains__(script):
            scriptToAdd = runnableMacro(script)
            if type(output := scriptToAdd.loadFile()) == str:
                return output
            self.scripts[script] = scriptToAdd
        return self.scripts[script].state != macroState.DISABLED

    def removeScript(self, script):
        if self.scripts.keys().__contains__(script):
            if self.scripts[script].state == macroState.DISABLED:
                self.scripts.pop(script)

    def startRecording(self, script):
        self.isRecording = True
        self.scriptRecording = script
        self.lastActionTime = time.time()
        self.lastTimeMoved = time.time()
        self.wasMouseMoved = False

    def stopRecording(self):
        self.isRecording = False
        output = ""
        # Save the list self.recording in the file macros/self.scriptRecording
        with open(os.path.join("macros", self.scriptRecording), 'w') as f:
            if self.scripts[self.scriptRecording].keybind != None:
                keybindText = f"keybind({self.scripts[self.scriptRecording].keybind})\n"
                f.write(keybindText)
                output += keybindText
            for line in self.recording:
                output += f"{line}\n"
            f.write(output)
        self.update(self.scriptRecording)
        self.recording = []
        self.scriptRecording = None
        self.lastActionTime = None
        self.lastMouseMoved = -1
        self.runningScripts = []
        return output

    def update(self, lastSelected):
        self.scripts[lastSelected].loadFile()

        

    def addTime(self):
        currentTime = time.time()
        self.recording.append(f"sleep({(currentTime - self.lastActionTime) / 1000})")
        self.lastActionTime = currentTime

    def onPress(self, key):
        # Send the keypress to every script that is not disabled for checking the keybind
        for script in self.scripts:
            if self.scripts[script].state != macroState.DISABLED:
                if (results := self.scripts[script].onKeyPress(key)) is bool:
                    if results:
                        self.runningScripts.append(script)
                    else:
                        self.runningScripts.remove(script)
        if self.isRecording:
            if self.firstMouseCoords:
                self.onMove(self.controllerMouse.position[0], self.controllerMouse.position[1])
                self.firstMouseCoords = False
            self.locker.acquire()
            self.addTime()
            # TODO every cases
            self.recording.append(f"write({key})")
            self.locker.release()

    # For recording
    def onMove(self, x, y):
        if self.isRecording:
            self.firstMouseCoords = True
            if (timeChanged := time.time() - self.lastActionTime) > self.moveMouseTime:
                self.locker.acquire()
                self.recording.append(f"moveMouse({x}, {y}, {timeChanged})")
                print(f"time passed {timeChanged}")
                self.lastActionTime = time.time()
                self.locker.release()
                print("Saved mouse")


    def onClick(self, x, y, button, pressed):
        if self.isRecording and pressed:
            if self.firstMouseCoords:
                self.onMove(self.controllerMouse.position[0], self.controllerMouse.position[1])
                self.firstMouseCoords = False
            self.locker.acquire()
            # TODO check for moveMouse
            self.onMove(x, y)
            if button == 0:
                self.recording.append(f"leftClick()")
            elif button == 1:
                self.recording.append(f"rightClick()")
            elif button == 2:
                self.recording.append(f"shift()") # ?? Oh well, my ai thing thinks it's right
            elif button == 3:
                self.recording.append(f"unshift()")
            self.locker.release()

    def onScroll(self, x, y, dx, dy):
        if self.isRecording:
            if self.firstMouseCoords:
                self.onMove(self.controllerMouse.position[0], self.controllerMouse.position[1])
                self.firstMouseCoords = False
            self.locker.acquire()
            # TODO check for moveMouse
            self.recording.append(f"moveMouse({x}, {y}, {(time.time() - self.lastActionTime) / 1000}")
            self.recording.append(f"scroll({dx}, {dy})")
            self.locker.release()


