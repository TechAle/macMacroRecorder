from PyQt5.QtWidgets import QHBoxLayout, QLabel
from pynput import keyboard

from dynamicActions.action.ActionLol import actionLol
from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class Write(actionLol):

    actionStr = "type"

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

    def parseWindow(self, inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        value = actionValue.args["value"]
        if oldArgs is not None and oldArgs["value"] == value:
            if inputValues[0].text().__len__() <= 1:
                value = inputValues[0].text()
        elif oldArgs is not None and value.__len__() > 1:
            value = oldArgs["value"]

        newAction = self.createAction(value, actionValue.comment)[0]
        b = QHBoxLayout()
        b.addWidget(QLabel("What to write:"))
        b.addWidget(inputValues[0])
        inputValues[0].setText(str(newAction.args["value"]))
        inputValues[0].show()
        layoutToAdd.addLayout(b)
        # Update the table
        changeTable(newAction.actionStr, str(newAction.args['value']))

        return layoutToAdd, newAction


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
        values = extra.split(")")
        if values.__len__() > 1:
            argoument = extra[0]
            if argoument.__len__() > 1:
                return False, "Len but be 1"
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