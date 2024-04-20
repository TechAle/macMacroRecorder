import os
from typing import Dict, List, Optional, Tuple, Any

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget


from variables.RunnableMacro import runnableMacro
from variables.actions import action


class displayText:
    def __init__(self, layout: QTableWidget):
        self.actions: List[action] = []
        self.table: QTableWidget = layout
        self.keybind: Optional[Any] = None
        self.svg: Dict[str, QIcon] = {}
        self.prepareSVG()

    def prepareSVG(self) -> None:
        # Load every SVG in the folder images in prepareSVG as QIcon
        for filename in os.listdir("images"):
            if filename.endswith(".svg"):
                self.svg[filename[:-4]] = QIcon(QPixmap(f"images/{filename}"))

    def getString(self) -> str:
        output = ""
        if self.keybind is not None:
            output += f"keybind({self.keybind.char})\n"
        for action in self.actions:
            action, args, comment = action.getValues()
            if action == "invalid":
                output += f"{args}\n"
            else:
                output += f"{action}({args}) #{comment}\n"
        return output

    def setString(self, text: str) -> None:
        # Reset table
        self.resetTable()
        macro = runnableMacro()
        output = macro.loadScript(text)
        self.keybind = macro.keybind
        self.actions = macro.script
        self.table.setRowCount(len(self.actions))
        idxRow = 0
        for action in self.actions:
            action, args, comment = action.getValues()
            self.table.setItem(idxRow, 0, self.getSvg(action))
            self.table.setItem(idxRow, 1, QTableWidgetItem(action))
            self.table.setItem(idxRow, 2, QTableWidgetItem(args))
            self.table.setItem(idxRow, 3, QTableWidgetItem(comment))
            idxRow += 1

    def getSvg(self, name: str) -> QTableWidgetItem:
        output = QIcon()
        if name in self.svg:
            output = self.svg[name]
        elif name == "moveMouse":
            output = self.svg["mouse"]
        elif name == "scroll":
            output = self.svg["middleClick"]
        elif name == "write" or name == "type":
            output = self.svg["keyboard"]
        else:
            output = self.svg["unknown"]
        item = QTableWidgetItem()
        item.setIcon(output)
        return item

    def resetTable(self) -> None:
        self.table.clearContents()
