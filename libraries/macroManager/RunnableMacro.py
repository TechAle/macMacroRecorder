import json
import os
import threading
from typing import Union

from pynput.keyboard import KeyCode

from libraries.dynamicActions.action.ActionManager import actionManager
from libraries.macroManager.MacroState import macroState


class runnableMacro(threading.Thread):
    def __init__(self, script: Union[str, None] = None, signalHander=None):
        self.managerAction = actionManager()
        if script is not None:
            threading.Thread.__init__(self)
            self.enabled: bool = False
            self.state: macroState = macroState.DISABLED
            self.scriptName: str = script
            self.idx: int = 0
            self.keybind: Union[KeyCode, None] = None
            self.argsRunnable = self.loadArgs()
            self.signalHander = signalHander
            self.scripts = []

    def loadFile(self) -> None | str:
        with open(os.path.join("macros", self.scriptName), 'r') as file:
            text: str = file.read()
            output = self.loadScript(text)
            if isinstance(output, str):
                return output
            return None

    def loadScript(self, text: str) -> Union[str, None]:
        self.managerAction.actions = []
        self.idx = 0
        self.keybind = None
        self.enabled = False
        self.output = ""
        self.managerAction.setCurrentRunning(self)
        idx = 0
        for line in text.split("\n"):
            idx += 1
            line = line.strip()
            if len(line) == 0:
                continue
            outputStr = self.managerAction.parseLine(line)
            if len(outputStr) > 0:
                if outputStr.startswith("keybind: "):
                    self.keybind = KeyCode(char=outputStr[len("keybind: ")])
                else:
                    self.output += f"Line {idx} {outputStr}\t"
        if self.output != "":
            return self.output
        return None

    def changeState(self, newState) -> None:
        self.state = newState

    def toggle(self) -> macroState:
        self.changeState(macroState.WAITING if self.state == macroState.DISABLED else macroState.DISABLED)
        return self.state

    def onKeyPress(self, key: Union[KeyCode, str]) -> Union[bool, None]:
        if self.keybind == key:
            self.changeState(macroState.RUNNING if self.state == macroState.WAITING else macroState.WAITING)
            if self.state == macroState.RUNNING:
                self.idx = 0
                thread = threading.Thread(target=self.run)
                thread.daemon = True
                thread.start()
                return True
            return False
        return None

    def run(self) -> None:
        while self.state == macroState.RUNNING:
            results = self.managerAction.actions[self.idx].run(self.argsRunnable)

            if "randomTemp" in results:
                self.argsRunnable["randomTemp"] = results["randomTemp"]
            elif "stop" in results:
                self.changeState(macroState.WAITING)

            self.idx = (self.idx + 1) % len(self.managerAction.actions)
        if self.signalHander is not None:
            self.signalHander.emit("updateButtons")
        print(self.state)

    def update(self):
        self.scripts = self.managerAction.actions

    def loadArgs(self):
        # Open configuration.json
        with open("configurations.json", "r") as file:
            data = json.load(file)
            return data["runableArgs"]
