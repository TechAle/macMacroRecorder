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
        self.customAction = None

    def setCustomAction(self, action: str) -> None:
        self.customAction = action

    def getActionstr(self) -> str:
        return self.actionStr if self.customAction is None else self.customAction

    @abstractmethod
    def setNewArgsFromString(self, args: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def save(displayText, table, inputValues, action):
        ...

    @staticmethod
    @abstractmethod
    def editWindow(inputValues, actionValue, oldArgs, select_combo, changeTable, newCommand, layoutToAdd):
        pass

    @staticmethod
    @abstractmethod
    def editTable(newArgs, displayText) -> tuple[bool, str]:
        ...

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

    @staticmethod
    @abstractmethod
    def isValid(newAegs: str | dict) -> bool:
        ...

    '''
        :return true if we can continue the macro. 
        :return false if we must stop the macro. 
        :return number for changing the random value
        :return str for keybind
    '''

    @abstractmethod
    def run(self, args: {}) -> dict:
        ...

    @abstractmethod
    def getValues(self) -> tuple[str, str, str]:
        ...

    @staticmethod
    def getSvg() -> str:
        return "unknown"

