import math
import random
import threading
import time

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem


from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController

from libraries.dynamicActions.action.ActionLol import actionLol


class MoveMouse(actionLol):

    actionStr = "moveMouse"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str) -> str:
        args = self.getString(args)
        if MoveMouse.isValid(args):
            self.args = args
        else:
            self.args = self.getDefaultArgs()
        return ""

    @staticmethod
    def tryFloat(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            return 0.0

    @staticmethod
    def getString(input: str | dict) -> {}:
        if type(input) == dict:
            return input
        input = input.split(",")
        if len(input) == 1:
            return {
                "x": MoveMouse.tryFloat(input[0]),
                "y": 0.0,
                "time": 0.0
            }
        elif len(input) == 2:
            return {
                "x": MoveMouse.tryFloat(input[0]),
                "y": MoveMouse.tryFloat(input[1]),
                "time": 0.0
            }
        return {
            "x": MoveMouse.tryFloat(input[0]),
            "y": MoveMouse.tryFloat(input[1]),
            "time": MoveMouse.tryFloat(input[2])
        }

    @staticmethod
    def isValid(newArgs: str | dict):
        try:
            if type(newArgs) == str:
                newArgs = newArgs.split(",")
                if len(newArgs) == 2:
                    return False
                float(newArgs[0])
                float(newArgs[1])
                float(newArgs[2])
                return True
            else:
                if "x" not in newArgs or "y" not in newArgs or "time" not in newArgs:
                    return False
                float(newArgs["x"])
                float(newArgs["y"])
                float(newArgs["time"])
                return True
        except ValueError:
            return False

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        if not MoveMouse.isValid(newArgs):
            return True, "This is not correct"
        actionChange.args = MoveMouse.getString(newArgs)
        return False, ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        displayText.actions[displayText.actions.index(action)].args = MoveMouse.getString(inputValues[0].text())
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(inputValues[0].text()))

    @staticmethod
    def dictSame(a, b):
        return "x" in a and "y" in a and "x" in b and "y" in b and a["x"] == b["x"] and a["y"] == b["y"] and \
                "time" in a and "time" in b

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args
        save = True
        if oldArgs is not None and MoveMouse.dictSame(oldArgs, value):
            if MoveMouse.isValid(inputValues[0].text()):
                value = MoveMouse.getString(inputValues[0].text())
            else:
                save = False
        elif oldArgs is not None:
            if MoveMouse.isValid(inputValues[0].text()):
                value = MoveMouse.getString(inputValues[0].text())
            else:
                save = False
        else:
            if MoveMouse.isValid(value):
                value = MoveMouse.getString(value)
            else:
                save = False

        newAction = MoveMouse.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("Time:"))
        b.addWidget(inputValues[0])
        if save:
            inputValues[0].setText(f"{newAction.args['x']}, {newAction.args['y']}, {newAction.args['time']}")
            changeTable(newAction.actionStr, f"{newAction.args['x']}, {newAction.args['y']}, {newAction.args['time']}")
        else:
            inputValues[0].setText(f"{value['x']},{value['y']}, {value['time']}")
            changeTable(value.actionStr, f"{value['x']}, {value['y']}, {value['time']}")
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        return layoutToAdd, newAction

    def run(self, args) -> dict:
        x, y = self.args["x"], self.args["y"]
        if self.args["time"] != 0:
            timeNeeded = self.args["time"] + random.uniform(0, args["randomTemp"]/1000)
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
        return {}

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), f"{self.args['x']}, {self.args['y']}, {self.args['time']}", self.comment

    @staticmethod
    def createAction(args: str | int, comment: str) -> tuple[actionLol, str]:
        output = MoveMouse()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[object, str]:
        extra = extra.split(")")
        try:
            if MoveMouse.isValid(extra[0]):
                other = '#'.join(')'.join(extra[1:]).split("#")[1:])
                return extra[0], other
            return False, "Error parsing"
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "x": 0.0,
            "y": 0.0,
            "time": 0.0
        }

    def getSvg(self) -> str:
        return "mouse"