from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem
from pynput import keyboard

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard, Key
from pynput.mouse import Controller as MouseController


class Type(actionLol):
    actionStr = "type"

    def __init__(self):
        super().__init__()
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = self.getDefaultArgs()
        self.comment = ""

    def setNewArgsFromString(self, args: str) -> str:
        if args != "":
            self.args["value"] = args
        else:
            self.args = self.getDefaultArgs()
        return ""

    @staticmethod
    def save(displayText, table, inputValues, action):
        displayText.actions[displayText.actions.index(action)].args["value"] = \
            inputValues[0].text()
        table.setItem(displayText.actions.index(action), 2,
                      QTableWidgetItem(inputValues[0].text()))

    @staticmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args["value"]
        if oldArgs is not None and oldArgs["value"] == value:
            inpValue = inputValues[0].text()
            if Type.isValid(inpValue):
                value = inpValue
        elif oldArgs is not None and not Type.isValid(oldArgs):
            value = oldArgs["value"]

        newAction = Type.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("What to write:"))
        b.addWidget(inputValues[0])
        inputValues[0].setText(str(newAction.args["value"]))
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        changeTable(newAction.actionStr, str(newAction.args['value']))

        return layoutToAdd, newAction

    @staticmethod
    def editTable(newArgs, actionChange) -> tuple[bool, str]:
        if not Type.isValid(newArgs):
            return True, "Value must be 1 character long"
        actionChange.args = {"value": newArgs}
        return False, ""

    @staticmethod
    def isValid(newArgs: str | dict):
        return newArgs["value"].__len__() <= 1 if type(newArgs) == dict else \
            True if type(newArgs) == str and newArgs.__len__() <= 1 else \
            hasattr(Key, newArgs)

    def run(self, args: {}) -> dict:
        if self.args["value"].__len__() == 1:
            self.controllerKeyboard.press(self.args["value"])
        elif self.args["value"].__len__() > 1:
            self.controllerKeyboard.press(getattr(Key, self.args["value"]))
        return {}

    def getValues(self) -> tuple[str, str, str]:
        return self.actionStr, self.args["value"], self.comment

    @staticmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        output = Type()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[str, str]:
        values = extra.split(")")
        if values.__len__() > 1:
            argoument = values[0]
            if argoument.__len__() > 1 and not hasattr(Key, argoument):
                return False, "Len but be 1 or be a Key"
            else:
                comment = values[1].split("#")
                if comment.__len__() > 1:
                    comment = '#'.join(comment[1:])
                else:
                    comment = ""
                return argoument, comment
        else:
            return False, "Incorrect syntax"

    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": ""
        }

    def getSvg(self) -> str:
        return "keyboard"
