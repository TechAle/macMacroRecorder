import os
import threading
from typing import Union

from pynput.keyboard import KeyCode

from dynamicActions.action.ActionManager import actionManager
from variables.MacroState import macroState
from variables.actions import action


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
            self.randomTemp: int = 0
            self.signalHander = signalHander

    def loadFile(self) -> None | str:
        with open(os.path.join("macros", self.scriptName), 'r') as file:
            text: str = file.read()
            output = self.loadScript(text)
            if isinstance(output, str):
                return output
            return None

    def loadScript(self, text: str) -> Union[str, None]:
        self.script = []
        self.idx = 0
        self.keybind = None
        self.enabled = False
        self.output = ""
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
                    self.script.append(action("invalid", args={"value": line}))
        if self.output != "":
            return self.output
        return None

    def toggle(self) -> Union[None, macroState]:
        self.state = macroState.WAITING if self.state == macroState.DISABLED else macroState.DISABLED
        return self.state

    def onKeyPress(self, key: Union[KeyCode, str]) -> Union[bool, None]:
        if self.keybind == key:
            self.state = macroState.RUNNING if self.state == macroState.WAITING else macroState.WAITING
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
            results = self.managerAction.actions[self.idx].run(self.randomTemp)
            if type(results) == int:
                self.randomTemp = results
            elif not results:
                self.state = macroState.WAITING
            else:
                self.idx = (self.idx + 1) % len(self.script)
        if self.signalHander is not None:
            self.signalHander.emit("updateButtons")
