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
        extra = extra.split(")")[0]
        if extra == "" or extra.__len__() > 1:
            return False, False
        return extra, ""


    @staticmethod
    def getDefaultArgs() -> {str: any}:
        ...
