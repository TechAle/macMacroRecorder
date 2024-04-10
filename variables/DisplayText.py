from PyQt5.QtWidgets import QLabel, QTableWidgetItem

from variables.RunnableMacro import runnableMacro


class displayText:
    def __init__(self, layout):
        super().__init__()
        self.actions = []
        self.table = layout
        self.keybind = None

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
                self.table.setItem(idxRow, 1, QTableWidgetItem(f"random"))
                self.table.setItem(idxRow, 2, QTableWidgetItem(f"{lastRandom}"))
                idxRow += 1
            self.table.setItem(idxRow, 1, QTableWidgetItem(widget[0]))
            self.table.setItem(idxRow, 2, QTableWidgetItem(widget[1]))
            idxRow += 1

    def resetTable(self):
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    self.table.removeItem(row, column)