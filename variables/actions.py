import math
import random
import threading
import time
from typing import Union, Dict, Any

from pynput import keyboard
from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class action:
    def __init__(self, action: str, args: Union[None, Dict[str, Any]] = None, comment: str = "") -> None:
        self.actionStr = action
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = args
        self.comment = comment

    def setNew(self, action: str, args: Union[None, Dict[str, Any]], comment: str = ""):
        self.actionStr = action
        self.args = args
        self.comment = comment

    def run(self, randomValue: float = 0) -> bool:
        if self.actionStr == "sleep":
            time.sleep(self.args["value"] + random.uniform(0, randomValue))
        elif self.actionStr == "random":
            return self.args["value"]
        elif self.actionStr == "rightClick":
            self.controllerMouse.press(Button.right)
            self.controllerMouse.release(Button.right)
        elif self.actionStr == "leftClick":
            self.controllerMouse.press(Button.left)
            self.controllerMouse.release(Button.left)
        elif self.actionStr == "shift":
            self.controllerKeyboard.press(Key.shift)
        elif self.actionStr == "scroll":
            self.controllerMouse.scroll(self.args["dx"], self.args["dy"])
        elif self.actionStr == "unshift":
            self.controllerKeyboard.release(Key.shift)
        elif self.actionStr == "middleClick":
            self.controllerMouse.press(Button.middle)
        elif self.actionStr == "stop":
            return False
        elif self.actionStr == "type":
            self.controllerKeyboard.press(self.args["value"])
            self.controllerKeyboard.release(self.args["value"])
        elif self.actionStr == "write":
            if self.args["value"].startswith("Key."):
                toPress = keyboard.HotKey.parse("<" + self.args["value"].split('.')[1] + ">")[0]
                self.controllerKeyboard.press(toPress)
                self.controllerKeyboard.release(toPress)
            else:
                self.controllerKeyboard.type(self.args["value"])
        elif self.actionStr == "moveMouse":
            x, y = self.args["x"], self.args["y"]
            if self.args["time"] != 0:
                timeNeeded = self.args["time"] + random.uniform(0, randomValue)
                stop = False

                def smoothMove(mouse: MouseController, x: float, y: float, timeNeeded: float) -> None:
                    currentX, currentY = mouse.position[0], mouse.position[1]
                    distance = math.sqrt((x - currentX) ** 2 + (y - currentY) ** 2)
                    if distance == 0:
                        return
                    duration = timeNeeded / distance
                    deltaX = (x - currentX) / distance
                    deltaY = (y - currentY) / distance
                    for i in range(int(distance - distance / 95)):
                        currentX += deltaX
                        currentY += deltaY
                        if stop:
                            break
                        mouse.position = (currentX, currentY)
                        time.sleep(duration)

                thread = threading.Thread(target=smoothMove, args=(self.controllerMouse, x, y, timeNeeded))
                thread.daemon = True
                thread.start()
                time.sleep(timeNeeded)
                stop = True
            self.controllerMouse.position = (x, y)
        return True

    def getValues(self) -> tuple[str, str, str]:
        args = ""
        if self.args is not None and len(self.args) > 0:
            if self.actionStr == "moveMouse":
                args = f"{self.args['x']},{self.args['y']},{self.args['time']}"
            elif self.actionStr == "scroll":
                args = f"{self.args['dx']},{self.args['dy']}"
            elif len(self.args) == 1:
                args = f"{self.args[list(self.args.keys())[0]]}"
            elif self.actionStr == "invalid":
                args = self.args["value"]
            else:
                print("Missing arguments for action " + self.actionStr + " args:" + str(self.args))
        return self.actionStr, args, self.comment
