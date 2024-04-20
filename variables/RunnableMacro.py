import os
import threading
from typing import Union

from pynput.keyboard import KeyCode

from variables.MacroState import macroState
from variables.actions import action


class runnableMacro(threading.Thread):
    def __init__(self, script: Union[str, None] = None):
        if script is not None:
            threading.Thread.__init__(self)
            self.enabled: bool = False
            self.state: macroState = macroState.DISABLED
            self.scriptName: str = script
            self.idx: int = 0
            self.script: list[action] = []
            self.keybind: Union[KeyCode, None] = None
            self.randomTemp: int = 0

    def loadFile(self) -> None | str:
        with open(os.path.join("macros", self.scriptName), 'r') as file:
            text: str = file.read()
            output = self.loadScript(text)
            if isinstance(output, str):
                return output
            return None

    def parseLine(self, line: str) -> tuple[bool, bool, bool] | tuple[str, str, str]:
        command = line.split('(')
        extra = '('.join(command[1:])
        command = command[0]
        argouments = ""
        comment = ""

        try:
            if command == "write":
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
                    argouments = extra[:output]
                    comment = extra[output + 1:]
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
        except Exception:
            return False, False, False

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
            command, argouments, comment = self.parseLine(line)
            if command is False:
                if self.output == "":
                    self.output = f"Syntax errors:"
                self.output += f"\tLine {idx}: {line}"
                self.script.append(action("invalid", args={"value": line}))
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
                if self.output == "":
                    self.output = f"Syntax errors:"
                self.output += f"\tLine {idx}: {line}"
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
            results = self.script[self.idx].run(self.randomTemp)
            if type(results) == int:
                self.randomTemp = results
            elif not results:
                self.state = macroState.WAITING
            else:
                self.idx = (self.idx + 1) % len(self.script)
