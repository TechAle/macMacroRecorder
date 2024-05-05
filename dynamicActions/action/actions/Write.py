from dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class Write(actionLol):

    actionStr = "write"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str) -> str:
        self.args["value"] = args
        return ""

    def save(self, displayText, table, inputValues):
        ...

    def parseWindow(self, inputValues, changeWindow, action, oldArgs):
        ...

    def run(self, args: {}) -> bool:
        ...

    def getValues(self) -> tuple[str, str, str]:
        ...

    @staticmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        output = Write()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, bool] | tuple[str, str]:
        skip = False
        output = -1
        for idx, character in enumerate(extra):
            if skip:
                skip = False
                continue
            if character == "\\":
                skip = True
            elif character == ")":
                output = idx
                break
        if output == -1:
            return False, False
        else:
            argouments = extra[:output]
            comment = extra[output + 1:]
            return argouments, comment

    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": ""
        }