from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as ControllerMouse

from variables.MacroState import macroState
from variables.RunnableMacro import runnableMacro


class macroManager():

    def __init__(self):
        self.scripts = {}
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = ControllerMouse()

    def onDrag(self, point):
        pass

    def onToggle(self, script):
        if not self.scripts.__contains__(script):
            return None
        return self.scripts[script].toggle()

    def onCreate(self, script):
        if not self.scripts.keys().__contains__(script):
            scriptToAdd = runnableMacro(script, ControllerKeyboard, ControllerMouse)
            if type(scriptToAdd.loadFile()) == str:
                return scriptToAdd.loadFile()
            self.scripts[script] = scriptToAdd
        return self.scripts[script].state != macroState.DISABLED

    def removeScript(self, script):
        if self.scripts.keys().__contains__(script):
            if self.scripts[script].state == macroState.DISABLED:
                self.scripts.pop(script)

    def onPress(self, key):
        # Send the keypress to every script that is not disabled for checking the keybind
        for script in self.scripts:
            if self.scripts[script].state != macroState.DISABLED:
                self.scripts[script].onKeyPress(key)
        # TODO record
