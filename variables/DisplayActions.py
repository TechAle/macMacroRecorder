from typing import Optional

from PyQt5 import Qt
from PyQt5.QtCore import Qt as tableQt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMenu, QPushButton,
)

from variables.DisplayText import displayText
from variables.actions import action
from variables.EditWindow import editWindow


# noinspection PyUnresolvedReferences
class TableWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, parent: any):
        super().__init__(rows, columns)
        self.setContextMenuPolicy(tableQt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.displayText: displayText | None = None
        self.parent: displayAction = parent
        self.windows: [editWindow] = []

    def setDisplayText(self, displayText):
        self.displayText = displayText

    def show_context_menu(self, pos: Qt.QPoint):
        menu = QMenu(self)
        actionEdit = menu.addAction("Edit")
        actionEdit.triggered.connect(lambda idx, pos_args=pos: self.edit_row(idx, pos_args))
        actionDelete = menu.addAction("Delete")
        actionDelete.triggered.connect(lambda idx, pos_args=pos: self.delete_row(idx, pos_args))
        # Add menu "add above" and "add below"
        actionAddAbove = menu.addAction("Add Above")
        actionAddAbove.triggered.connect(lambda idx, pos_args=pos: self.add_above(idx, pos_args))
        actionAddBelow = menu.addAction("Add Below")
        actionAddBelow.triggered.connect(lambda idx, pos_args=pos: self.add_below(idx, pos_args))
        # Add menu "move up" and "move down"
        actionMoveUp = menu.addAction("Move Up")
        actionMoveUp.triggered.connect(lambda idx, pos_args=pos: self.move_up(idx, pos_args))
        actionMoveDown = menu.addAction("Move Down")
        actionMoveDown.triggered.connect(lambda idx, pos_args=pos: self.move_down(idx, pos_args))
        # Add separator
        menu.addSeparator()
        menu.exec_(self.mapToGlobal(pos))

    def edit_row(self, idx: int, pos: Qt.QPoint):
        item = self.itemAt(pos)
        if item:
            print(f"Cell: {item.row()}, {item.column()}")
            # Create a new window
            self.windows.append(editWindow(self.displayText, self.displayText.actions[item.row()], self))
            self.windows[-1].show()

    def removeWindow(self, window: editWindow):
        self.windows.remove(window)


    def delete_row(self, idx: int, pos: Qt.QPoint):
        item = self.itemAt(pos)
        if item:
            toRemove = item.row()
            # Remove the row
            self.removeRow(toRemove)
            # Also remove it from actions
            self.displayText.actions.pop(toRemove)

    def add_above(self, idx: int, pos_args: Qt.QPoint):
        item = self.itemAt(pos_args)
        if item:
            toAdd = item.row()
            self.addEmpty(toAdd)

    def addEmpty(self, row):
        # Add the row
        # Insert a row with in every column "invalid"
        self.insertRow(row)
        # Edit the first column with the text "invalid"
        self.parent.beforeRollback = False
        self.setItem(row, 1, QTableWidgetItem("invalid"))
        self.setItem(row, 0, self.parent.displayText.getSvg("invalid"))
        # Also add it to actions
        self.displayText.actions.insert(row, action("invalid", args={"value": ""}))

    def add_below(self, idx: int, pos_args: Qt.QPoint):
        item = self.itemAt(pos_args)
        if item:
            toAdd = item.row()
            self.addEmpty(toAdd + 1)

    def move_up(self, idx: int, pos_args: Qt.QPoint):
        # Move a row up by 1
        item = self.itemAt(pos_args)
        if item:
            toMove = item.row()
            self.swapRows(toMove, -1)

    def swapRows(self, row: int, offset: int):
        if offset == 0:
            return
        newRow = row + offset
        # Backup for the row that is gonna get overwritten
        command = self.item(newRow, 1).text()
        arguments = self.item(newRow, 2).text()
        comment = self.item(newRow, 3).text()
        # Add a new row above
        self.parent.disableCheck = True
        self.setItem(newRow, 0, self.parent.displayText.getSvg(self.item(row, 1).text()))
        self.setItem(newRow, 1, QTableWidgetItem(self.item(row, 1).text()))
        self.setItem(newRow, 2, QTableWidgetItem(self.item(row, 2).text()))
        self.setItem(newRow, 3, QTableWidgetItem(self.item(row, 3).text()))
        # And now row
        self.setItem(row, 0, self.parent.displayText.getSvg(command))
        self.setItem(row, 1, QTableWidgetItem(command))
        self.setItem(row, 2, QTableWidgetItem(arguments))
        self.setItem(row, 3, QTableWidgetItem(comment))
        self.parent.disableCheck = False





    def move_down(self, idx: int, pos_args: Qt.QPoint):
        item = self.itemAt(pos_args)
        if item:
            toMove = item.row()
            self.swapRows(toMove, 1)


class displayAction(QWidget):
    def __init__(self):
        super().__init__()
        # Set the size policy of the widget to expanding
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create table
        self.beforeRollback = True
        self.disableCheck = False
        self.table = TableWidget(1, 4, self)

        # Set column names
        self.table.setHorizontalHeaderLabels(["", "Command", "Arguments", "Comments"])

        header = self.table.horizontalHeader()
        header.setMaximumSectionSize(400)
        self.table.setColumnWidth(0, 50)
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
        # Add a button to layout for keybind
        self.keybindButton = QPushButton("Keybind: ")

        # Create layout and add table
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.keybindButton)
        self.displayText = displayText(self.table, self.keybindButton)
        self.table.setDisplayText(self.displayText)

        # Connect the cellChanged signal to a slot
        self.loading = False
        # noinspection PyUnresolvedReferences
        self.table.cellChanged.connect(self.cell_edited)
        # Create a locker
        self.revertBackup: Optional[QTableWidget] = None

    def backupCommit(self):
        new_table = QTableWidget(self.table.rowCount(), self.table.columnCount())
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    new_item = QTableWidgetItem(item.text())
                    new_item.setData(tableQt.ItemDataRole.UserRole, item.data(tableQt.ItemDataRole.UserRole))
                    new_table.setItem(row, column, new_item)
        self.revertBackup = new_table

    def cell_edited(self, row: int, column: int) -> bool | str:
        returnValue: str  = ""
        if not self.beforeRollback:
            self.beforeRollback = True
            return
        if self.loading or self.disableCheck:
            return
        rollback = False
        if column == 0:
            rollback = True
        else:
            # This slot will be called whenever a cell gets edited
            print(f"Cell at row {row} and column {column} has been edited.")
            # TODO shift all this into action function or an utility
            # TODO give a feedback when errors are made
            # TODO having random create lots of desyncs
            # Edit action
            if column == 1:
                newAction: None | QTableWidgetItem | str = self.table.item(row, column)
                if newAction is None:
                    return
                newAction = newAction.text()
                if not newAction in [
                    "sleep",
                    "rightClick",
                    "leftClick",
                    "shift",
                    "scroll",
                    "unshift",
                    "middleClick",
                    "stop",
                    "type",
                    "write",
                    "moveMouse",
                ]:
                    rollback = True
                    print(f"Invalid action: {newAction}")
                    returnValue = f"Invalid action: {newAction}"
                else:
                    actionReplace = None
                    if newAction in ["rightClick", "leftClick", "shift", "unshift", "middleClick", "stop"]:
                        self.displayText.actions[row].setNew(newAction, {})
                    elif newAction in ["write", "type"]:
                        self.displayText.actions[row].setNew(newAction, {"value": "a"})
                    elif newAction == "random":
                        self.displayText.actions[row].setNew(newAction, {"value": 0})
                    elif newAction == "moveMouse":
                        self.displayText.actions[row].setNew(newAction, {"x": 0, "y": 0, "time": 0})
                    elif newAction == "sleep":
                        self.displayText.actions[row].setNew(newAction, {"time": 0})
                    elif newAction == "scroll":
                        self.displayText.actions[row].setNew(newAction, {"dx": 0, "dy": 0})
                    elif newAction == "random":
                        self.displayText.actions[row].setNew(newAction, {"value": 0})
                    elif newAction == "invalid":
                        rollback = True
                    else:
                        print("I forgot an action " + newAction)
            # Edit arguments
            elif column == 2:
                actionConsidered: None | QTableWidgetItem | str = self.table.item(row, 1)
                if actionConsidered is None:
                    return
                actionConsidered = actionConsidered.text()
                if actionConsidered in [
                    "rightClick",
                    "leftClick",
                    "shift",
                    "scroll",
                    "unshift",
                    "middleClick",
                    "stop",
                ]:
                    newArgs = self.table.item(row, column).text()
                    if newArgs != "":
                        rollback = True
                        print("They cannot have arguments")
                        returnValue = "They cannot have arguments"
                elif actionConsidered == "write" or actionConsidered == "type":
                    newArgs = self.table.item(row, column).text()
                    if newArgs == "":
                        rollback = True
                        print("Invalid arguments: " + newArgs)
                        returnValue = "Invalid arguments: " + newArgs
                    self.displayText.actions[row].args = {"value": newArgs}
                elif actionConsidered == "moveMouse":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs) != 3:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                    # Check if every argument is a number or float
                    try:
                        newDict = {"x": float(newArgs[0]), "y": float(newArgs[1]), "time": float(newArgs[2])}
                        self.displayText.actions[row].args = newDict
                    except ValueError:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                elif actionConsidered == "scroll":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs) != 2:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                    # Check if every argument is a number or float
                    try:
                        newDict = {"dx": float(newArgs[0]), "dy": float(newArgs[1])}
                        self.displayText.actions[row].args = newDict
                    except ValueError:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                elif actionConsidered == "sleep" or actionConsidered == "random":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs) != 1:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                    newArgs = newArgs[0]
                    # Check if every argument is a number or float
                    try:
                        self.displayText.actions[row].args["value"] = float(newArgs)
                    except ValueError:
                        rollback = True
                        print("Invalid arguments: " + str(newArgs))
                        returnValue = "Invalid arguments: " + str(newArgs)
                elif actionConsidered == "invalid":
                    newArgs = self.table.item(row, column).text()
                    self.displayText.actions[row].args["value"] = newArgs
                else:
                    rollback = True
                    print(f"Invalid action: {actionConsidered}")
                    returnValue = f"Invalid action: {actionConsidered}"
            # Edit comments
            elif column == 3:
                value = self.table.item(row, column)
                if value is None:
                    return
                self.displayText.actions[row].comment = value.text()

            if not rollback:
                self.backupCommit()
        if rollback:
            # Get the original text of the cell
            original_text = self.revertBackup.item(row, column).text()
            # Set the cell's text back to its original value
            self.beforeRollback = False
            self.table.item(row, column).setText(original_text)
            return returnValue if len(returnValue) > 0 else False
        return True

    def toPlainText(self) -> str:
        return self.displayText.getString()

    def setPlainText(self, text: str):
        self.loading = True
        self.displayText.setString(text)
        self.loading = False
        self.backupCommit()
