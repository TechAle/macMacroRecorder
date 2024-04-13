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

    def parseLine(self, line):
        command = line.split('(')
        extra = '('.join(command[1:])
        command = command[0]
        argouments = ""
        comment = ""

        if command == "write":
            # Iterate for every character of command
            skip = False
            output = -1
            for idx, character in enumerate(extra):
                if skip:
                    skip = False
                    continue
                if character == "\\":
                    skip = True
                elif character == ")":
                    output = idx
                    break
            if output == -1:
                return False, False, False
            else:
                argouments = extra[:output + 1]
                comment = extra[output + 2:]
        elif command == "type":
            argouments = extra[0]
            comment = extra[2:]
        else:
            temp = extra.split(")")
            argouments = temp[0]
            comment = temp[1]

        comment = comment.split("#")
        if len(comment) >= 1:
            comment = ''.join(comment[1:])
        else:
            comment = ""
        return command, argouments, comment

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
            command, argouments, comment = self.parseLine(line)
            if command is False:
                return f"Syntax error at line {idx}: {line}"
            elif command == "random":
                self.script.append(action(command, args={
                    "value": float(argouments)
                }, comment=comment))
            elif command == "keybind":
                self.keybind = KeyCode.from_char(argouments.replace("\"", "").replace("'", "")[0])
            elif command == "write" or command == "type":
                temp = action(command,
                              args={
                                  "value": argouments
                              }, comment=comment)
                self.script.append(temp)
            # Everything that does not have any argouments
            elif ["leftClick", "rightClick", "middleClick"].__contains__(command):
                self.script.append(action(command, comment=comment))
            elif command == "scroll":
                x, y = argouments.strip().replace(" ", "").split(",")
                self.script.append(action(command, args={
                    "dx": float(x),
                    "dy": float(y)
                }, comment=comment))
            elif command == "random" or command == "sleep":
                self.script.append(action(command,
                                          args={
                                              "value": float(argouments)
                                          }, comment=comment))
            elif command == "moveMouse":
                x, y, speed = argouments.split(',')
                self.script.append(action(command,
                                          args={
                                              "x": float(x),
                                              "y": float(y),
                                              "time": float(speed)
                                          }, comment=comment))
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
