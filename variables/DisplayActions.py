import threading

from PyQt5 import Qt

from PyQt5.QtCore import Qt as tableQt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QSizePolicy, QScrollArea, QTableWidget, \
    QTableWidgetItem, QHeaderView, QMenu

from variables.DisplayText import displayText
from variables.actions import action


class TableWidget(QTableWidget):
    def __init__(self, columns, rows):
        super().__init__(columns, rows)
        self.setContextMenuPolicy(tableQt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        actionEdit = menu.addAction("Edit")
        actionEdit.triggered.connect(lambda idx, pos_args=pos: self.print_row_index(idx, pos_args))
        actionDelete = menu.addAction("Delete")
        actionDelete.triggered.connect(lambda idx, pos_args=pos: self.delete_row(idx, pos_args))
        menu.exec_(self.mapToGlobal(pos))

    def print_row_index(self, idx, pos):
        item = self.itemAt(pos)
        if item:
            print(f"Cell: {item.row()}, {item.column()}")

    def delete_row(self, idx, pos):
        item = self.itemAt(pos)
        if item:
            print(f"Cell: {item.row()}, {item.column()}")


class displayAction(QWidget):


    def __init__(self):
        super().__init__()
        # Set the size policy of the widget to expanding
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create table
        self.table = TableWidget(5, 4)  # 5 rows, 4 columns

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

        # Create layout and add table
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.displayText = displayText(self.table)

        # Connect the cellChanged signal to a slot
        self.loading = False
        self.table.cellChanged.connect(self.cell_edited)
        # Create a locker
        self.locker = threading.Lock()
        self.revertBackup = None
        self.beforeRollback = True

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

    def cell_edited(self, row, column):
        if not self.beforeRollback:
            self.beforeRollback = True
            return
        if self.loading:
            return
        roolback = False
        if column == 0:
            roolback = True
        else:
            # This slot will be called whenever a cell gets edited
            print(f"Cell at row {row} and column {column} has been edited.")
            # TODO shift all this into action function or an utility
            # TODO give a feedback when errors are made
            # TODO having random create lots of desyncs
            # Edit action
            if column == 1:
                newAction = self.table.item(row, column).text()
                if not newAction in ["sleep", "right", "left", "shift", "scroll", "unshift", "middleClick", "stop", "type", "write", "moveMouse"]:
                    roolback = True
                    print(f"Invalid action: {newAction}")
                else:
                    actionReplace = None
                    if newAction in ["right", "left", "shift", "unshift", "middleClick", "stop"]:
                        actionReplace = action(newAction)
                    elif newAction in ["write", "type"]:
                        actionReplace = action(newAction, {"value": "a"})
                    elif newAction == "random":
                        actionReplace = action(newAction, {"value": 0})
                    elif newAction == "moveMouse":
                        actionReplace = action(newAction, {
                            "x": 0,
                            "y": 0,
                            "time": 0
                        })
                    elif newAction == "sleep":
                        actionReplace = action(newAction,  {
                            "time": 0
                        })
                    elif newAction == "scroll":
                        actionReplace = action(newAction,  {
                            "dx": 0,
                            "dy": 0
                        })
                    elif newAction == "random":
                        actionReplace = action(newAction,  {
                            "value": 0
                        })
                    else:
                        print("I forgot an action " + newAction)
                    self.displayText.actions[row] = actionReplace
            # Edit argouments
            elif column == 2:
                actionConsiderated = self.table.item(row, 1).text()
                actionConsiderated = actionConsiderated
                if actionConsiderated in ["right", "left", "shift", "scroll", "unshift", "middleClick", "stop"]:
                    roolback = True
                    print("They cannot have arguments")
                elif actionConsiderated == "write" or actionConsiderated == "type":
                    newArgs = self.table.item(row, column).text()
                    if newArgs == "":
                        roolback = True
                        print("Invalid arguments: " + newArgs)
                    self.displayText.actions[row].args = {"value": newArgs}
                elif actionConsiderated == "moveMouse":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs)!= 3:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))
                    # Check if every argument is a number or float
                    try:
                        newDict = {
                            "x": float(newArgs[0]),
                            "y": float(newArgs[1]),
                            "time": float(newArgs[2])
                        }
                        self.displayText.actions[row].args = newDict
                    except ValueError:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))
                elif actionConsiderated == "scroll":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs)!= 2:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))
                    # Check if every argument is a number or float
                    try:
                        newDict = {
                            "dx": float(newArgs[0]),
                            "dy": float(newArgs[1])
                        }
                        self.displayText.actions[row].args = newDict
                    except ValueError:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))
                elif actionConsiderated == "sleep" or actionConsiderated == "random":
                    newArgs = self.table.item(row, column).text()
                    newArgs = newArgs.split(",")
                    if len(newArgs)!= 1:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))
                    newArgs = newArgs[0]
                    # Check if every argument is a number or float
                    try:
                        self.displayText.actions[row].args["value"] = float(newArgs)
                    except ValueError:
                        roolback = True
                        print("Invalid arguments: " + str(newArgs))

                else:
                    roolback = True
                    print(f"Invalid action: {actionConsiderated}")
            # Edit comments
            elif column == 3:
                ...


            if not roolback:
                self.backupCommit()
        if roolback:
            # Get the original text of the cell
            original_text = self.revertBackup.item(row, column).text()
            # Set the cell's text back to its original value
            self.beforeRollback = False
            self.table.item(row, column).setText(original_text)


    def toPlainText(self):
        return self.displayText.getString()

    def setPlainText(self, text):
        self.loading = True
        self.displayText.setString(text)
        self.loading = False
        self.backupCommit()
