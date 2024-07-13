from PyQt5.QtWidgets import QHBoxLayout, QLabel, QTableWidgetItem
from pynput import keyboard

from libraries.dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController


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
            value = inputValues[0].text()
        newAction = Write.createAction(value, actionValue.comment)[0]
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
        actionChange.args = {"value": newArgs}
        return False, ""

    @staticmethod
    def isValid(newArgs):
        return True

    def run(self, args: {}) -> bool | int:
        if self.args["value"].startswith("Key."):
            toPress = keyboard.HotKey.parse("<" + self.args["value"].split('.')[1] + ">")[0]
            self.controllerKeyboard.press(toPress)
            self.controllerKeyboard.release(toPress)
        else:
            self.controllerKeyboard.type(self.args["value"])
        return True

    def getValues(self) -> tuple[str, str, str]:
        return self.actionStr, self.args["value"], self.comment

    @staticmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        output = Write()
        output.comment = comment
        error = output.setNewArgsFromString(args)
        return output, error

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[str, str]:
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
            return False, "Incorrect brackets"
        else:
            argouments = extra[:output]
            comment = extra[output + 1:]
            comment = comment.strip()[1:]
            return argouments, comment

    @staticmethod
    def getDefaultArgs() -> {str: any}:
        return {
            "value": ""
        }

    @staticmethod
    def getSvg() -> str:
        return "keyboard"