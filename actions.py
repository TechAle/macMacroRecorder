import random
import time

import macmouse
from pynput.keyboard import Key


class action:
    def __init__(self, action, random, controller):
        self.actionStr = action
        self.random = random
        self.controller = controller

    def run(self) -> bool:
        if self.actionStr.__contains__("sleep"):
            time.sleep(float(self.actionStr.split("(")[1][:-1]) + random.uniform(0, self.random))
        elif self.actionStr == "right":
            macmouse.click(button="right")
        elif self.actionStr == "left":
            macmouse.click(button="left")
        elif self.actionStr == "shift":
            self.controller.press(Key.shift)
        elif self.actionStr == "unshift":
            self.controller.release(Key.shift)
        elif self.actionStr == "stop":
            return True
        else:
            self.controller.type(self.actionStr)
        return False