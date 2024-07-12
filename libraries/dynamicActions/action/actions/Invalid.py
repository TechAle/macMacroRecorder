from pynput import keyboard

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


class Invalid(actionLol):

    actionStr = "invalid"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str) -> str:
        self.args["value"] = args
        return ""

    @staticmethod
    def isValid(self, newArgs):
        return True

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        actionChange.args = {"value": newArgs}
        return False, ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        ...

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        newAction = Invalid.createAction(newCommand, actionValue.comment)[0]
        changeTable(newAction.actionStr, "")
        return None, newAction

    def run(self, args: {}) -> bool | int:
        if self.args["value"].startswith("Key."):
            toPress = keyboard.HotKey.parse("<" + self.args["value"].split('.')[1] + ">")[0]
            self.controllerKeyboard.press(toPress)
            self.controllerKeyboard.release(toPress)
        else:
            self.controllerKeyboard.type(self.args["value"])
        return True

    def getValues(self) -> tuple[str, str, str]:
        return self.getActionstr(), self.args["value"], self.comment

    @staticmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        output = Invalid()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[str, str]:
        extra = extra.split(")")
        if extra.__len__() == 1:
            return extra[0], ""
        else:
            other = '#'.join(')'.join(extra[1:]).split("#")[1:])
            return extra[0], other

    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
        }