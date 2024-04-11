import os

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QTableWidgetItem

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
        lastRandom = 0
        if self.keybind is not None:
            output += f"keybind({self.keybind.char})\n"
        for action in self.actions:
            if action.random != lastRandom:
                lastRandom = action.random
                output += f"random({lastRandom})\n"
            output += action.__str__() + "\n"
        return output

    def setString(self, text):
        # Reset table
        self.resetTable()
        macro = runnableMacro()
        macro.loadScript(text)
        self.keybind = macro.keybind
        self.actions = macro.script
        lastRandom = 0
        idxRow = 0
        for action in self.actions:
            widget = str(action)
            widget = widget[:-1].split("(")
            if action.random != lastRandom:
                lastRandom = action.random
                self.table.setItem(idxRow, 0, self.getSvg("random"))
                self.table.setItem(idxRow, 1, QTableWidgetItem(f"random"))
                self.table.setItem(idxRow, 2, QTableWidgetItem(f"{lastRandom}"))
                idxRow += 1
            self.table.setItem(idxRow, 0, self.getSvg(widget[0]))
            self.table.setItem(idxRow, 1, QTableWidgetItem(widget[0]))
            self.table.setItem(idxRow, 2, QTableWidgetItem(widget[1]))

    def getSvg(self, name):
        output = QIcon()
        if name in self.svg:
            output = self.svg[name]
        if name == "moveMouse":
            output = self.svg["mouse"]
        if name == "scroll":
            output = self.svg["middleClick"]
        item = QTableWidgetItem()
        item.setIcon(output)
        return item



    def resetTable(self):
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    self.table.removeItem(row, column)