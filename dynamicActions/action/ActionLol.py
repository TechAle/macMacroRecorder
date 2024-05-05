# Create abstract class
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union, Dict, Any, TypeVar

from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class actionLol(ABC):
    actionStr = ""

    def __init__(self, args: Union[None, Dict[str, any]] = None, comment: str = "") -> None:
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = args
        self.comment = comment

    def setNew(self, action: str, args: Union[None, Dict[str, any]], comment: str = ""):
        self.actionStr = action
        self.args = args
        self.comment = comment

    @abstractmethod
    def setNewArgsFromString(self, args: str) -> str:
        ...

    @abstractmethod
    def save(self, displayText, table, inputValues):
        ...

    @abstractmethod
    def parseWindow(self, inputValues, changeWindow, action, oldArgs):
        pass

    @staticmethod
    @abstractmethod
    def getDefaultArgs() -> {str: any}:
        ...

    @staticmethod
    @abstractmethod
    def createAction(args: str, comment: str) -> tuple[actionLol, str]:
        ...

    '''
        Checks if the structure of the argouments is correct
    '''

    @staticmethod
    def parseLine(extra: str) -> tuple[bool, str] | tuple[str, str]:
        ...

    '''
        :return true if we can continue the macro. 
        :return false if we must stop the macro. 
        :return number for changing the random value
        :return str for keybind
    '''

    @abstractmethod
    def run(self, args: {}) -> bool | int | str:
        ...

    @abstractmethod
    def getValues(self) -> tuple[str, str, str]:
        ...


'''
    This function basically checks if the brackets are correct, and if so the middle value
    :return True/False if it's correct or not, and then the middle value
'''
def parseLine(line: str) -> tuple[bool, str]:
    valid = False
    for i in line:
        if i == ")" and not valid:
            valid = True
        elif i == ")" and valid:
            return False, "Too many )"
        elif i == "#":
            break
    if not valid:
        return False, "There is not a )"
    return True, line.split(')')[0]
