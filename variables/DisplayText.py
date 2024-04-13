import os

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidgetItem

from variables.RunnableMacro import runnableMacro


class displayText:
    def __init__(self, layout):
        super().__init__()
        self.actions = []
        self.table = layout
        self.keybind = None
        self.svg = {}
        self.prepareSVG()

    def prepareSVG(self):
        # Load every SVG in the folder images in prepareSVG as QIcon
        for filename in os.listdir("images"):
            if filename.endswith(".svg"):
                self.svg[filename[:-4]] = QIcon(QPixmap(f"images/{filename}"))

    def getString(self):
        output = ""
        if self.keybind is not None:
            output += f"keybind({self.keybind.char})\n"
        for action in self.actions:
            action, args, comment = action.getValues()
            output += f"{action}({args}) #{comment}\n"
        return output

    def setString(self, text):
        # Reset table
        self.resetTable()
        macro = runnableMacro()
        macro.loadScript(text)
        self.keybind = macro.keybind
        self.actions = macro.script
        self.table.setRowCount(self.actions.__len__())
        idxRow = 0
        for action in self.actions:
            action, args, comment = action.getValues()
            self.table.setItem(idxRow, 0, self.getSvg(action))
            self.table.setItem(idxRow, 1, QTableWidgetItem(action))
            self.table.setItem(idxRow, 2, QTableWidgetItem(args))
            self.table.setItem(idxRow, 3, QTableWidgetItem(comment))
            idxRow += 1

    def getSvg(self, name):
        output = QIcon()
        if name in self.svg:
            output = self.svg[name]
        elif name == "moveMouse":
            output = self.svg["mouse"]
        elif name == "scroll":
            output = self.svg["middleClick"]
        elif name == "write" or name == "type":
            output = self.svg["keyboard"]
        item = QTableWidgetItem()
        item.setIcon(output)
        return item



    def resetTable(self):
        self.table.clearContents()