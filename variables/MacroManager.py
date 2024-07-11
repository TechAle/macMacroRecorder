import os
import threading
import time
from typing import Dict, Union, List

from pynput.keyboard import Controller as ControllerKeyboard, KeyCode
from pynput.mouse import Controller as ControllerMouse

from variables.MacroState import macroState
from variables.RunnableMacro import runnableMacro


class macroManager:

    def __init__(self, moveMouseTime: float, signalHander):
        self.scripts: Dict[str, runnableMacro] = {}
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = ControllerMouse()
        self.isRecording: bool = False
        self.scriptRecording: Union[str, None] = None
        self.recording: List[str] = []
        self.lastActionTime: Union[float, None] = None
        self.lastTimeMoved: Union[float, None] = None
        self.firstMouseCoords: bool = False
        self.locker = threading.Lock()
        self.moveMouseTime: float = moveMouseTime
        self.scriptRecording: Union[str, None] = None
        self.lastMouseMoved: int = -1
        self.runningScripts: [runnableMacro] = []
        self.signalHander = signalHander

    def onToggle(self, script: str) -> Union[None, macroState]:
        if script not in self.scripts:
            return None
        return self.scripts[script].toggle()

    def onCreate(self, script: str, update: bool = False) -> Union[bool, str]:
        if script not in self.scripts.keys():
            scriptToAdd = runnableMacro(script, self.signalHander)
            output = scriptToAdd.loadFile()
            if isinstance(output, str):
                return output
            self.scripts[script] = scriptToAdd
        elif update:
            output = self.update(script)
            if output is not None:
                return output
        return self.scripts[script].state != macroState.DISABLED

    def removeScript(self, script: str) -> None:
        if script in self.scripts.keys():
            if self.scripts[script].state == macroState.DISABLED:
                self.scripts.pop(script)

    def startRecording(self, script: str) -> None:
        self.isRecording = True
        self.scriptRecording = script
        self.lastActionTime = time.time()
        self.lastTimeMoved = time.time()
        self.recording = []
        self.firstMouseCoords = False

    def stopRecording(self) -> str:
        self.isRecording = False
        output = ""
        temp = None
        for idx, line in enumerate(self.recording):
            if "moveMouse" in line:
                b = line.split(' ')[:-1]
                b.append(" 0)")
                temp = (idx, " ".join(b))
                break
        if temp is not None:
            self.recording[temp[0]] = temp[1]
        with open(os.path.join("macros", self.scriptRecording), 'w') as f:
            if self.scripts[self.scriptRecording].keybind is not None:
                keybindText = f"keybind({self.scripts[self.scriptRecording].keybind.char})\n"
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

    def update(self, lastSelected: str) -> None | str:
        return self.scripts[lastSelected].loadFile()

    def addTime(self) -> None:
        currentTime = time.time()
        self.recording.append(f"sleep({(currentTime - self.lastActionTime) / 1000})")
        self.lastActionTime = currentTime

    def onPress(self, key: Union[KeyCode, None]) -> bool:
        change = False
        for script in self.scripts:
            if self.scripts[script].state != macroState.DISABLED:
                if isinstance(output := self.scripts[script].onKeyPress(key), bool):
                    if output:
                        self.runningScripts.append(script)
                        change = True
                    else:
                        self.runningScripts.remove(script)
                        change = True
        if self.isRecording:
            if self.firstMouseCoords:
                self.onMove(self.controllerMouse.position[0], self.controllerMouse.position[1])
                self.firstMouseCoords = False
            self.locker.acquire()
            self.addTime()
            if isinstance(key, KeyCode):
                self.recording.append(f"type({key.char})")
            else:
                self.recording.append(f"write({key})")
            self.locker.release()
        return change

    def onMove(self, x: int, y: int) -> None:
        if self.isRecording:
            self.firstMouseCoords = True
            if (timeChanged := time.time() - self.lastActionTime) > self.moveMouseTime:
                self.locker.acquire()
                self.recording.append(f"moveMouse({x}, {y}, {timeChanged})")
                self.lastActionTime = time.time()
                self.locker.release()

    def onClick(self, x: int, y: int, button, pressed: bool) -> None:
        if self.isRecording and pressed:
            if self.firstMouseCoords:
                self.onMove(x, y)
                self.firstMouseCoords = False
            self.locker.acquire()
            if button.name == "left":
                self.recording.append(f"leftClick()")
            elif button.name == "right":
                self.recording.append(f"rightClick()")
            elif button.name == "middle":
                self.recording.append(f"middleClick()")
            self.locker.release()

    def onScroll(self, x: int, y: int, dx: int, dy: int) -> None:
        if self.isRecording:
            if self.firstMouseCoords:
                self.onMove(self.controllerMouse.position[0], self.controllerMouse.position[1])
                self.firstMouseCoords = False
            self.locker.acquire()
            self.recording.append(f"moveMouse({x}, {y}, {(time.time() - self.lastActionTime) / 1000})")
            self.recording.append(f"scroll({dx}, {dy})")
            self.locker.release()

    def isRunning(self) -> bool:
        for script in self.scripts:
            if self.scripts[script].state == macroState.RUNNING:
                return True
        return False
