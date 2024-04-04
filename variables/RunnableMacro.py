import os
import threading

from variables.actions import action


class runnableMacro(threading.Thread):
    def __init__(self, script, ControllerKeyboard, ControllerMouse):
        threading.Thread.__init__(self)
        self.enabled = False
        self.keybind = None
        self.running = False
        self.scriptName = script
        self.randomTime = 0
        self.idx = 0
        self.script = []
        self.controllerKeyboard = ControllerKeyboard
        self.controllerMouse = ControllerMouse

    def loadFile(self):
        with open(os.path.join("macros", self.scriptName), 'r') as file:
            idx = 0
            for line in file:
                idx += 1
                line = line.strip()
                if len(line) == 0:
                    continue
                line = line[:-1]
                line = line.split('(')
                if line.__len__() <= 1 :
                    return f"Syntax error at line {idx}: {line}"
                elif line[0] == "random":
                    self.randomTime = float(line[1])
                elif line[0] == "keybind":
                    self.keybind = line[1]
                elif line[0] == "leftClick":
                    self.script = action(line[0], self.randomTime, self.controllerMouse, self.controllerKeyboard)
                elif line[0] == "rightClick":
                    self.script = action(line[0], self.randomTime, self.controllerMouse, self.controllerKeyboard)
                elif line[0] == "write":
                    self.script = action(line[0], self.randomTime, self.controllerMouse, self.controllerKeyboard)



    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def enable(self, key):
        if key == self.keybind:
            self.running = not self.running


    def run(self):
        while self.enabled:
            pass