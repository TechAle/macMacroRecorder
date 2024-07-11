from libraries.dynamicActions.action import ActionLol
from libraries.dynamicActions.action.ActionLol import actionLol


class Write(actionLol):
    actionStr = "keybind"

    def setNewArgsFromString(self, args: str) -> str:
        ...

    def save(self, displayText, table, inputValues):
        ...

    def editWindow(self, inputValues, changeWindow, action, oldArgs):
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
