import time

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


class Scroll(actionLol):

    actionStr = "scroll"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str) -> str:
        args = self.getString(args)
        if Scroll.isValid(args):
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
                "dx": Scroll.tryFloat(input[0]),
                "dy": 0.0
            }
        return {
            "dx": Scroll.tryFloat(input[0]),
            "dy": Scroll.tryFloat(input[1])
        }

    @staticmethod
    def isValid(newArgs: str | dict):
        try:
            if type(newArgs) == str:
                newArgs = newArgs.split(",")
                if len(newArgs) == 1:
                    return False
                float(newArgs[0])
                float(newArgs[1])
                return True
            else:
                if "dx" not in newArgs or "dy" not in newArgs:
                    return False
                float(newArgs["dx"])
                float(newArgs["dy"])
                return True
        except ValueError:
            return False

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        if not Scroll.isValid(newArgs):
            return True, "This is not correct"
        actionChange.args = Scroll.getString(newArgs)
        return False, ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        displayText.actions[displayText.actions.index(action)].args = Scroll.getString(inputValues[0].text())
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(inputValues[0].text()))

    @staticmethod
    def dictSame(a, b):
        return "dx" in a and "dy" in a and "dx" in b and "dy" in b and a["dx"] == b["dx"] and a["dy"] == b["dy"]

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args
        save = True
        if oldArgs is not None and Scroll.dictSame(oldArgs, value):
            if Scroll.isValid(inputValues[0].text()):
                value = Scroll.getString(inputValues[0].text())
            else:
                save = False
        elif oldArgs is not None:
            if Scroll.isValid(inputValues[0].text()):
                value = Scroll.getString(inputValues[0].text())
            else:
                save = False
        else:
            if Scroll.isValid(value):
                value = Scroll.getString(value)
            else:
                save = False

        newAction = Scroll.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("Time:"))
        b.addWidget(inputValues[0])
        if save:
            inputValues[0].setText(f"{newAction.args['dx']}, {newAction.args['dy']}")
            changeTable(newAction.actionStr, f"{newAction.args['dx']}, {newAction.args['dy']}")
        else:
            inputValues[0].setText(f"{value['dx']},{value['dy']}")
            changeTable(newAction.actionStr, f"{value['dx']}, {value['dy']}")
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        return layoutToAdd, newAction

    def run(self, args) -> dict:
        self.controllerMouse.scroll(self.args["dx"], self.args["dy"])
        return {}

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), f"{self.args['dx']}, {self.args['dy']}", self.comment

    @staticmethod
    def createAction(args: str | int, comment: str) -> tuple[actionLol, str]:
        output = Scroll()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[object, str]:
        extra = extra.split(")")
        try:
            if Scroll.isValid(extra[0]):
                other = '#'.join(')'.join(extra[1:]).split("#")[1:])
                return extra[0], other
            return False, "Error parsing"
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "dx": 0.0,
            "dy": 0.0
        }

    def getSvg(self) -> str:
        return "middleClick"