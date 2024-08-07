import time
from random import Random

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem
from pynput import keyboard

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


class Sleep(actionLol):

    actionStr = "sleep"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""
        self.random = Random()

    def setNewArgsFromString(self, args: str | int | float) -> str:
        if Sleep.isValid({"value": args}):
            self.args["value"] = float(args)
        else:
            self.args = self.getDefaultArgs()
        return ""

    @staticmethod
    def isValid(newArgs: str | dict):
        try:
            return float(newArgs["value"]) if type(newArgs) == dict else float(newArgs)
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
                value = float(inputValues[0].text())
            except ValueError:
                save = False
        elif oldArgs is not None:
            try:
                value = float(inputValues[0].text())
            except ValueError:
                save = False
        else:
            try:
                value = float(value)
            except ValueError:
                save = False

        newAction = Sleep.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("Time:"))
        b.addWidget(inputValues[0])
        if save:
            inputValues[0].setText(str(newAction.args["value"]))
        else:
            inputValues[0].setText(str(Sleep.getDefaultArgs()["value"]))
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        changeTable(newAction.actionStr, str(newAction.args['value']))

        return layoutToAdd, newAction

    def run(self, args) -> dict:
        time.sleep(self.args["value"]/1000 + self.random.randint(0, args["randomTemp"])/1000)
        return {}

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), str(self.args["value"]), self.comment

    @staticmethod
    def createAction(args: str | int | float, comment: str) -> tuple[actionLol, str]:
        output = Sleep()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[object, str]:
        extra = extra.split(")")
        try:
            value = float(extra[0])
            other = '#'.join(')'.join(extra[1:]).split("#")[1:])
            return value, other
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": 0
        }