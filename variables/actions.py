import math
import random
import threading
import time

from pynput.keyboard import Key
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


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
            self.controllerMouse.press(Button.right)
        elif self.actionStr == "left":
            self.controllerMouse.press(Button.left)
        elif self.actionStr == "shift":
            self.controllerKeyboard.press(Key.shift)
        elif self.actionStr == "unshift":
            self.controllerKeyboard.release(Key.shift)
        elif self.actionStr == "middleClick":
            self.controllerMouse.press(Button.middle)
        # Maybe if i want add the option for button 8-30 lol
        elif self.actionStr == "stop":
            return False
        elif self.actionStr == "write":
            self.controllerKeyboard.type(self.args["text"])
        # Add option for moving the mouse
        elif self.actionStr == "moveMouse":
            x, y = self.args["x"], self.args["y"]
            if self.args["time"] != 0:
                '''
                    My plan is this: I want to move the mouse at position in exactly timeNeeded time
                    And i also want a smooth movement
                    So, for achieving this, i create a thread that will smoothly move the mouse there
                    Till the last step, the last step will be done after timeNeeded time
                    And to be 100% accurate i create a thread for doing that movement slowly
                    And the main wait timeNeeded time and then move the mouse
                '''
                timeNeeded = self.args["time"] + random.uniform(0, self.random)
                stop = False
                # Create function smoothMove

                def smoothMove(mouse, x, y, timeNeeded):
                    # Move the mouse in x, y in timeNeeded time in a smooth way
                    currentX, currentY = mouse.position[0], mouse.position[1]
                    distance = math.sqrt((x - currentX)**2 + (y - currentY)**2)
                    if distance == 0:
                        return
                    duration = timeNeeded / distance
                    deltaX = (x - currentX) / distance
                    deltaY = (y - currentY) / distance
                    # Print distance
                    print("Distance: ", math.sqrt((x - currentX)**2 + (y - currentY)**2))
                    for i in range(int(distance - distance/95)):
                        currentX += deltaX
                        currentY += deltaY
                        if stop:
                            break
                        mouse.position = (currentX, currentY)
                        time.sleep(duration)

                # Pass some arguments to the function
                thread = threading.Thread(target=smoothMove, args=(self.controllerMouse, x, y, timeNeeded))
                thread.setDaemon(True)
                thread.start()


                time.sleep(timeNeeded)
                stop = True


            self.controllerMouse.position = (x, y)





        return True