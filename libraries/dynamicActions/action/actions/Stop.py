import time
from random import Random

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem
from pynput import keyboard

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


class Stop(actionLol):

    actionStr = "stop"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str | int) -> str:
        return ""

    @staticmethod
    def isValid(newArgs: str | dict):
        if newArgs.__len__() == 0:
            return True
        return False

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        return True, "This cannot have args"

    @staticmethod
    def save(displayText, table, inputValues, action):
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(""))

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        newAction = Stop.createAction("", actionValue.comment)[0]
        # Update the table
        changeTable(newAction.actionStr, "")

        return layoutToAdd, newAction

    def run(self, args) -> dict:
        return {"stop": True}

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), "", self.comment

    @staticmethod
    def createAction(args: str | int, comment: str) -> tuple[actionLol, str]:
        output = Stop()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[object, str]:
        extra = extra.split(")")
        try:
            value = ""
            other = '#'.join(')'.join(extra[1:]).split("#")[1:])
            return value, other
        except ValueError:
            return False, "Value must be an integer"


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return ""