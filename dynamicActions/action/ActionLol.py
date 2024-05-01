# Create abstract class
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union, Dict, Any, TypeVar

from pynput.keyboard import Key, Controller as ControllerKeyboard
from pynput.mouse import Controller as MouseController, Button


class actionLol(ABC):

    def __init__(self, action: str, args: Union[None, Dict[str, any]] = None, comment: str = "") -> None:
        self.actionStr = action
        self.controllerKeyboard = ControllerKeyboard()
        self.controllerMouse = MouseController()
        self.args = args
        self.comment = comment

    def setNew(self, action: str, args: Union[None, Dict[str, any]], comment: str = ""):
        self.actionStr = action
        self.args = args
        self.comment = comment

    @abstractmethod
    def setNewFromString(self, args: str) -> str:
        ...

    @abstractmethod
    def save(self, displayText, table, inputValues):
        ...

    @abstractmethod
    def parseWindow(self, inputValues, changeWindow, action, oldArgs):
        pass

    @abstractmethod
    def getDefault(self) -> actionLol:
        ...

    @abstractmethod
    def createAction(self, command: str, argouments: str, comment: str) -> tuple[actionLol, str]:
        ...

    @abstractmethod
    def parseLine(self, line: str) -> tuple[bool, bool, bool] | tuple[str, str, str]:
        ...

    @abstractmethod
    def run(self, args: {}) -> bool:
        ...

    @abstractmethod
    def getValues(self) -> tuple[str, str, str]:
        ...
