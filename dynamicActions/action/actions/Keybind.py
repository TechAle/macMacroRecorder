from pynput import keyboard

from dynamicActions.action import ActionLol
from dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class Write(actionLol):
    actionStr = "keybind"

    def setNewArgsFromString(self, args: str) -> str:
        ...

    def save(self, displayText, table, inputValues):
        ...

    def parseWindow(self, inputValues, changeWindow, action, oldArgs):
        ...

    def run(self, args: {}) -> bool | int:
        ...

    def getValues(self) -> tuple[str, str, str]:
        ...

    @staticmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        ...

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, bool] | tuple[str, str]:
        output = ActionLol.parseLine(extra)
        if output[0]:
            return output[1], ""
        else:
            return False, False

    @staticmethod
    def getDefaultArgs() -> {str: any}:
        ...
