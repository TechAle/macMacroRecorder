import os
from typing import Dict, List

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QInputDialog, QMessageBox
from pynput.keyboard import KeyCode

from dynamicActions.action import ActionLol
from variables.RunnableMacro import runnableMacro


class displayText:
    def __init__(self, layout: QTableWidget, keybindButton: QPushButton):
        self.actions: List[ActionLol] = []
        self.table: QTableWidget = layout
        self.keybind: KeyCode | None = None
        self.svg: Dict[str, QIcon] = {}
        self.keybindButton: QPushButton = keybindButton
        self.keybindButton.clicked.connect(self.keybindButtonClicked)
        self.prepareSVG()

    def keybindButtonClicked(self) -> None:
        # Ask to the user for a new string
        new_keybind, ok = QInputDialog.getText(self.table, 'New Keybind', 'Enter the keybind:')  # type: str, int
        if ok:
            if not new_keybind:
                # Reset keybind
                self.keybind = None
                self.keybindButton.setText("Keybind: ")
                # Say that the keybind has been resetted
                QMessageBox.information(self.table, "Feedback", "Keybind resetted",
                                        QMessageBox.Ok)
            elif len(new_keybind) == 1:
                # Create the new keybind
                self.keybind = KeyCode(char=new_keybind)
                self.keybindButton.setText(f"keybind: {new_keybind}")
                # Say that the keybind has changed
                QMessageBox.information(self.table, "Feedback", f"Keybind changed to {new_keybind}",
                                        QMessageBox.Ok)
            else:
                QMessageBox.information(self.table, "Feedback", "The keybind must be 1 long",
                                        QMessageBox.Abort)
        else:
            QMessageBox.information(self.table, "Feedback", "Cancelled successfully",
                                    QMessageBox.Ok)

    def prepareSVG(self) -> None:
        # Load every SVG in the folder images in prepareSVG as QIcon
        for filename in os.listdir("images"):
            if filename.endswith(".svg"):
                self.svg[filename[:-4]] = QIcon(QPixmap(f"images/{filename}"))

    def getString(self) -> str:
        output = ""
        if self.keybind is not None:
            keybindReplace = self.keybind.char.replace("\'", "")
            output += f"keybind({keybindReplace})\n"
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
        if self.keybind is not None:
            self.keybindButton.setText(f"keybind: {self.keybind.char}")
        self.actions = macro.managerAction.actions
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
