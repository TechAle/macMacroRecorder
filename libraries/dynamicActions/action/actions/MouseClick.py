import time

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


class MouseClick(actionLol):

    actionStr = "mouseClick"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    @staticmethod
    def getString(input: str | dict) -> {}:
        if type(input) == dict:
            return input
        input = input.split(",")
        if len(input) == 1:
            return {
                "value": int(input[0]),
                "pressed": 0
            }
        return {
            "value": int(input[0]),
            "pressed": int(input[1])
        }

    def setNewArgsFromString(self, args: str | int | dict) -> str:
        if MouseClick.isValid(args):
            if type(args) == dict:
                self.args = args
            else:
                self.args["value"] = int(args.split(",")[0])
                self.args["pressed"] = int(args.split(",")[1])
        else:
            self.args = self.getDefaultArgs()
        return ""

    @staticmethod
    def isValid(newArgs: str | dict):
        try:
            if type(newArgs) == dict:
                return "value" in newArgs and "pressed" in newArgs and int(newArgs["value"]) and int(newArgs["pressed"]) in [0, 1]
            else:
                newArgs = newArgs.split(",")
                int(newArgs[0])
                return len(newArgs) == 2 and int(newArgs[1]) in [0, 1]
        except ValueError:
            return False

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        actionChange.args = {"value": int(newArgs.split(",")[0]),
                             "pressed": int(newArgs.split(",")[1])}
        return False, ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        displayText.actions[displayText.actions.index(action)].args = MouseClick.getString(inputValues[0].text())
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(inputValues[0].text()))

    @staticmethod
    def isSame(a, b):
        return "value" in a and "pressed" in a and "value" in b and "pressed" in b and a["value"] == b["value"] and a["pressed"] == b["pressed"]

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args
        save = True
        if oldArgs is not None and MouseClick.isSame(oldArgs, value):
            if MouseClick.isValid(inputValues[0].text()):
                value = MouseClick.getString(inputValues[0].text())
            else:
                save = False
        elif oldArgs is not None:
            if MouseClick.isValid(oldArgs):
                value = oldArgs
            else:
                save = False
        else:
            if MouseClick.isValid(value):
                value = MouseClick.getString(value)
            else:
                save = False

        newAction = MouseClick.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("Time:"))
        b.addWidget(inputValues[0])
        inputValues[0].setText(f"{newAction.args['value']}, {newAction.args['pressed']}")
        changeTable(newAction.actionStr, f"{newAction.args['value']}, {newAction.args['pressed']}")
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table

        return layoutToAdd, newAction

    def run(self, args) -> dict:
        return {
            "randomTemp": self.args["value"]
        }

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), str(self.args["value"]) + ", " + str(self.args["pressed"]), self.comment

    @staticmethod
    def createAction(args: str | int, comment: str) -> tuple[actionLol, str]:
        output = MouseClick()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[object, str]:
        extra = extra.split(")")
        try:
            if MouseClick.isValid(extra[0]):
                other = '#'.join(')'.join(extra[1:]).split("#")[1:])
                return extra[0], other
            return False, "Value must be integer"
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": 0,
            "pressed": 0
        }

    def getSvg(self) -> str:
        if self.args["value"] == 0:
            return "leftClick"
        elif self.args["value"] == 1:
            return "rightClick"
        elif self.args["value"] == 2:
            return "middleClick"
        return "mouse"