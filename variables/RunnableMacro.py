import os
import threading

from pynput.keyboard import KeyCode

from variables.MacroState import macroState
from variables.actions import action


class runnableMacro(threading.Thread):
    def __init__(self, script=None):
        if script is not None:
            threading.Thread.__init__(self)
            self.enabled = False
            self.state = macroState.DISABLED
            self.scriptName = script
            self.idx = 0
            self.script = []
            self.keybind = None
            self.randomTemp = 0

    def loadFile(self):
        with open(os.path.join("macros", self.scriptName), 'r') as file:
            text = file.read()
            self.loadScript(text)

    def loadScript(self, text):
        self.script = []
        self.idx = 0
        self.keybind = None
        self.enabled = False
        idx = 0
        for line in text.split("\n"):
            idx += 1
            line = line.strip()
            if len(line) == 0:
                continue
            line = line[:-1]
            line = line.split('(')
            if line.__len__() <= 1:
                return f"Syntax error at line {idx}: {line}"
            elif line[0] == "random":
                self.script.append(action(line[0], args={"value": float(line[1])}))
            elif line[0] == "keybind":
                self.keybind = KeyCode.from_char(line[1].replace("\"", "").replace("'", "")[0])
            elif line[0] == "write" or line[0] == "type":
                temp = action(line[0],
                                          args={
                                              "value": line[1]
                                          })
                self.script.append(temp)
            # Everything that does not have any argouments
            elif ["leftClick", "rightClick", "middleClick"].__contains__(line[0]):
                self.script.append(action(line[0]))
            elif line[0] == "scroll":
                x, y = line[1].strip().replace(" ", "").split(",")
                self.script.append(action(line[0], args={
                    "dx": float(x),
                    "dy": float(y)
                }))
            elif line[0] == "random" or line[0] == "sleep":
                self.script.append(action(line[0],
                                          args={
                                              "value": float(line[1])
                                          }))
            elif line[0] == "moveMouse":
                x, y, speed = line[1].split(',')
                self.script.append(action(line[0],
                                          args={
                                              "x": float(x),
                                              "y": float(y),
                                              "time": float(speed)
                                          }))
            else:
                return f"Unknown command at line {idx}: {line}"

    # When the toggle button is pressed
    def toggle(self):
        self.state = macroState.WAITING if self.state == macroState.DISABLED else macroState.DISABLED
        return self.state

    # For actually starting the thread/stopping it
    def onKeyPress(self, key):
        if self.keybind == key:
            self.state = macroState.RUNNING if self.state == macroState.WAITING else macroState.WAITING
            if self.state == macroState.RUNNING:
                self.idx = 0
                thread = threading.Thread(target=self.run)
                thread.daemon = True  # Daemonize the thread to stop it with the main application
                thread.start()
                return True
            return False
        return None

    def run(self):
        while self.state == macroState.RUNNING:
            results = self.script[self.idx].run(self.randomTemp)
            if type(results) == int:
                self.randomTemp = results
            elif not self.script[self.idx].run(self.randomTemp, self.randomTemp):
                self.state = macroState.WAITING
            else:
                self.idx = (self.idx + 1) % self.script.__len__()
