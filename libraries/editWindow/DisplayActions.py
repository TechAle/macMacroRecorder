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

from libraries.editWindow.DisplayText import displayText
from libraries.editWindow.EditWindow import editWindow

from libraries.dynamicActions.action.ActionManager import actionManager

# noinspection PyUnresolvedReferences
class TableWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, parent: any):
        super().__init__(rows, columns)
        self.setContextMenuPolicy(tableQt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.displayText: displayText | None = None
        self.parent: displayAction = parent
        self.windows: [editWindow] = []
        self.idxSwap = -1
        self.actionManager = actionManager()

    def setDisplayText(self, displayText):
        self.displayText = displayText

    def show_context_menu(self, pos: Qt.QPoint):
        menu = QMenu(self)
        actionEdit = menu.addAction("Edit")
        actionEdit.triggered.connect(lambda idx, pos_args=pos: self.edit_row(idx, pos_args))
        actionDelete = menu.addAction("Delete")
        actionDelete.triggered.connect(lambda _: self.delete_rows())
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
        if self.idxSwap == -1:
            actionMoveDown = menu.addAction("First swap")
            actionMoveDown.triggered.connect(lambda idx, pos_args=pos: self.setSwapFirst(idx, pos_args))
        else:
            actionMoveDown = menu.addAction("Reset first Down")
            actionMoveDown.triggered.connect(lambda idx, pos_args=pos: self.setSwapFirst(idx, pos_args))
            actionMoveDown = menu.addAction("Swap")
            actionMoveDown.triggered.connect(lambda idx, pos_args=pos: self.swap(idx, pos_args))
        # Add separator
        menu.addSeparator()
        menu.exec_(self.mapToGlobal(pos))

    def setSwapFirst(self, idx: int, pos: Qt.QPoint):
        item = self.itemAt(pos)
        if item:
            self.idxSwap = item.row()

    def swap(self, idx: int, pos: Qt.QPoint):
        item = self.itemAt(pos)
        if item:
            toSwap = item.row()
            self.swapRows(self.idxSwap, toSwap - self.idxSwap)
            self.idxSwap = -1

    def edit_row(self, idx: int, pos: Qt.QPoint):
        item = self.itemAt(pos)
        if item:
            action = self.displayText.actions[item.row()]
            for window in self.windows:
                if window.isAction(action):
                    window.activateWindow()
                    window.raise_()
                    return
            # Create a new window
            self.windows.append(editWindow(self.displayText, action, self))
            self.windows[-1].show()

    def removeWindow(self, window: editWindow):
        self.windows.remove(window)

    def delete_rows(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        selected_rows = set(index.row() for index in selected_indexes)
        for row in sorted(selected_rows, reverse=True):
            self.delete_row(row)

    def delete_row(self, toRemove: int):
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
        self.parent.disableCheck = True
        self.setItem(row, 1, QTableWidgetItem("invalid"))
        self.setItem(row, 0, self.parent.displayText.getSvg("invalid"))
        # Also add it to actions
        self.displayText.actions.insert(row, self.actionManager.actionsInstancer["invalid"].createAction("invalid", "")[0])
        self.parent.disableCheck = False

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
        command = self.item(newRow, 1)
        if type(command) is None:
            return
        command = command.text()
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

    def closeWindows(self):
        for window in self.windows:
            window.close()

    def onItemEdit(self, param):
        for window in self.windows:
            window.onItemEdit(param)


class displayAction(QWidget):
    def __init__(self):
        super().__init__()
        # Set the size policy of the widget to expanding
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create table
        self.beforeRollback = True
        self.disableCheck = False
        self.changeColumn1 = False
        self.table = TableWidget(1, 4, self)
        self.actionManager = actionManager()

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
        returnValue: str = ""
        if not self.beforeRollback:
            self.beforeRollback = True
            return
        if self.loading or self.disableCheck:
            return
        rollback = False
        if column == 0:
            if not self.changeColumn1:
                rollback = True
            else:
                return
        else:
            # This slot will be called whenever a cell gets edited
            print(f"Cell at row {row} and column {column} has been edited.")
            # TODO give a feedback when errors are made
            # Edit action
            if column == 1:
                newAction: None | QTableWidgetItem | str = self.table.item(row, column)
                if newAction is None:
                    return
                newAction = newAction.text()
                if not self.actionManager.actionsInstancer.__contains__(newAction):
                    rollback = True
                    print(f"Invalid action: {newAction}")
                    returnValue = f"Invalid action: {newAction}"
                elif newAction != self.displayText.actions[row].getActionstr():
                    self.displayText.actions[row] = self.actionManager.actionsInstancer[newAction].createAction("", self.displayText.actions[row].comment)[0]
                else:
                    return
            # Edit arguments
            elif column == 2:
                actionConsidered: None | QTableWidgetItem | str = self.table.item(row, 1)
                if actionConsidered is None:
                    return
                rollback, returnValue = self.actionManager.onCellEdit(actionConsidered.text(), self.table.item(row, column).text(), self.displayText.actions[row])
                if returnValue == "" and self.displayText.actions[row].actionStr != actionConsidered.text():
                    self.displayText.actions[row] = \
                        self.actionManager.actionsInstancer[actionConsidered.text()] \
                        .createAction(self.table.item(row, column).text(),
                                     self.displayText.actions[row].comment)[0]
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
            original_text = self.revertBackup.item(row, column)
            if original_text is None:
                original_text = "invalid"
            else:
                original_text = original_text.text()
            # Set the cell's text back to its original value
            self.beforeRollback = False
            self.table.item(row, column).setText(original_text)
            return returnValue if len(returnValue) > 0 else False
        else:
            self.table.onItemEdit(self.displayText.actions[row])
            self.changeColumn1 = True
            self.table.setItem(row, 0, self.displayText.getSvg(self.displayText.actions[row]))
            self.changeColumn1 = False
        return True

    def toPlainText(self) -> str:
        return self.displayText.getString()

    def setPlainText(self, text: str):
        self.table.closeWindows()
        self.loading = True
        self.displayText.setString(text)
        self.loading = False
        self.backupCommit()

    def updatePlainText(self):
        self.table.closeWindows()
        self.loading = True
        self.displayText.updateString()
        self.loading = False
        self.backupCommit()
