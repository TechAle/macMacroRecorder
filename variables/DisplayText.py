import os

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QTableWidgetItem, QMessageBox, QMenu, QTableWidget

from variables.RunnableMacro import runnableMacro




class displayText:
    def __init__(self, layout):
        super().__init__()
        self.actions = []
        self.table = layout
        self.keybind = None
        self.svg = {}
        self.prepareSVG()

        # Connect the clicked signal to a slot that handles the left-click event
        self.table.clicked.connect(self.handleLeftClick)

        # Define a method to handle the left-click event
    def handleLeftClick(self, pos):
        # Display an alert when you left-click a row
        print("left click " + str(pos))

        # Define a method to handle the right-click event
    def contextMenuEvent(self, event):
        # Prevent the default context menu from appearing
        event.ignore()

        print("right click")

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
                # TODO maybe try to center this
                self.table.setItem(idxRow, 0, self.getSvg("random"))
                self.table.setItem(idxRow, 1, QTableWidgetItem(f"random"))
                self.table.setItem(idxRow, 2, QTableWidgetItem(f"{lastRandom}"))
                idxRow += 1
            self.table.setItem(idxRow, 0, self.getSvg(widget[0]))
            self.table.setItem(idxRow, 1, QTableWidgetItem(widget[0]))
            self.table.setItem(idxRow, 2, QTableWidgetItem(widget[1]))
            idxRow += 1

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
        self.table.clearContents()