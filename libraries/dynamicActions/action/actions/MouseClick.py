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

    def setNewArgsFromString(self, args: str | int) -> str:
        if MouseClick.isValid({"value": args}):
            self.args["value"] = int(args)
        else:
            self.args = self.getDefaultArgs()
        return ""

    @staticmethod
    def isValid(newArgs: str | dict):
        try:
            return int(newArgs["value"]) if type(newArgs) == dict else int(newArgs)
        except ValueError:
            return False

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        actionChange.args = {"value": newArgs}
        return False, ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        displayText.actions[displayText.actions.index(action)].args["value"] = \
            inputValues[0].text()
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(inputValues[0].text()))

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args["value"]
        save = True
        if oldArgs is not None and oldArgs["value"] == value:
            try:
                value = int(inputValues[0].text())
            except ValueError:
                save = False
        elif oldArgs is not None:
            try:
                value = int(inputValues[0].text())
            except ValueError:
                save = False
        else:
            try:
                value = int(value)
            except ValueError:
                save = False

        newAction = MouseClick.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("Time:"))
        b.addWidget(inputValues[0])
        if save:
            inputValues[0].setText(str(newAction.args["value"]))
        else:
            inputValues[0].setText(str(MouseClick.getDefaultArgs()["value"]))
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        changeTable(newAction.actionStr, str(newAction.args['value']))

        return layoutToAdd, newAction

    def run(self, args) -> dict:
        return {
            "randomTemp": self.args["value"]
        }

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), self.args["value"], self.comment

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
            value = int(extra[0])
            other = '#'.join(')'.join(extra[1:]).split("#")[1:])
            return value, other
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": 0
        }

    def getSvg(self) -> str:
        if self.args["value"] == 0:
            return "leftClick"
        elif self.args["value"] == 1:
            return "rightClick"
        elif self.args["value"] == 2:
            return "middleClick"
        return "mouse"