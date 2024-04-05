import random
import time

import macmouse
from pynput.keyboard import Key
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


# TODO make some extends
class action:
    def __init__(self, action, random, args=None):
        self.actionStr = action
        self.random = random
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = args


    def run(self) -> bool:
        if self.actionStr.__contains__("sleep"):
            time.sleep(self.args["time"] + random.uniform(0, self.random))
        elif self.actionStr == "right":
            macmouse.click(button="right")
        elif self.actionStr == "left":
            macmouse.click(button="left")
        elif self.actionStr == "shift":
            self.controllerKeyboard.press(Key.shift)
        elif self.actionStr == "unshift":
            self.controllerKeyboard.release(Key.shift)
        elif self.actionStr == "stop":
            return False
        elif self.actionStr == "write":
            self.controllerKeyboard.type(self.args["text"])
        # Add option for moving the mouse
        elif self.actionStr == "moveMouse":
            x, y = self.args["x"], self.args["y"]
            speed = self.args["speed"] + random.uniform(0, self.random)
            # TODO manage speed later
            self.controllerMouse.position = (x, y)
        return True