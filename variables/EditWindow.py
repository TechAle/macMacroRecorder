from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QMessageBox, \
    QTableWidgetItem, QHBoxLayout

from dynamicActions.action.ActionManager import actionManager
from variables.DisplayText import displayText
from variables.actions import action


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.hide()
        else:
            clear_layout(item.layout())


class editWindow(QMainWindow):

    def __init__(self, displayText: displayText, action, father):
        super().__init__()
        self.setWindowTitle("New Window")
        self.displayText: displayText = displayText
        self.action = action
        self.father = father
        # I think i will never need more then 10 QLineEdit for the inputs
        self.inputValues: [QLineEdit] = [QLineEdit() for x in range(10)]
        self.oldArgs: dict[str, any] | None = None
        self.actionManager = actionManager()

        # Label with select box
        select_label = QLabel("Select:")
        self.addingItems: bool = True
        self.isEditing: bool = False
        self.comment: None | str = None
        self.oldIndex: int = -1
        self.select_combo = QComboBox()
        self.select_combo.currentIndexChanged.connect(self.on_combo_box_changed)

        self.argoumentsInputs = QVBoxLayout()

        comment_label = QLabel("Comments:")
        self.comment_input = self.inputValues[-1]

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(select_label)
        layout.addWidget(self.select_combo)
        layout.addLayout(self.argoumentsInputs)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_input)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.updateLayout()
        self.setCentralWidget(central_widget)

    def isAction(self, item: action):
        return self.action == item

    # This function is called by the table when a row gets updated, is needed for the sync
    def onItemEdit(self, item: action):
        if self.isAction(item) and not self.isEditing:
            self.updateLayout()

    def updateLayout(self):
        action, args, comment = self.action.getValues()

        # Every items in the select box
        # TODO make this list more accessible to everyon
        items = self.actionManager.getActionsStr()

        self.select_combo.clear()
        # With addingItems we ignore the call of on_combo_box_changed
        self.addingItems = True
        self.select_combo.addItems(items)
        self.comment = comment
        self.select_combo.setCurrentIndex(items.index(action))
        self.comment = None
        self.addingItems = False
        # Due to on_combo_box_changed not being called by us, for passing argouments we have to set a global varabiable
        self.on_combo_box_changed(items.index(action))

        self.comment_input.setText(comment)

    def on_combo_box_changed(self, index: int) -> None:
        # If we have to ignore the combo box changed
        if self.addingItems:
            return
        if index == -1:
            return
        layoutToAdd = QVBoxLayout()

        # Check every commands
        newCommand = self.select_combo.currentText()
        layoutToAdd, newAction = self.actionManager.parseWindow(self.inputValues, self.action, self.oldArgs, newCommand,
                                                                self.select_combo, self.changeTable, newCommand,
                                                                layoutToAdd)

        if ["left", "rightClick", "middleClick"].__contains__(newCommand):
            newAction = action(newCommand)
            self.changeTable(newAction.actionStr, "")
        elif newCommand == "scroll":
            if self.action.actionStr == "scroll":
                dx = self.action.args["dx"]
                dy = self.action.args["dy"]
                if self.oldArgs is None or (self.oldArgs["dx"] == dx and self.oldArgs["dy"] == dy):
                    try:
                        dx = float(self.inputValues[0].text())
                    # This is how you check if the str is a float
                    except ValueError:
                        pass
                    try:
                        dy = float(self.inputValues[1].text())
                    except ValueError:
                        pass
                newAction = action(newCommand, args={
                    "dx": dx,
                    "dy": dy
                })
            else:
                newAction = action(newCommand, args={
                    "dx": 0,
                    "dy": 0
                })
            b = QHBoxLayout()
            b.addWidget(QLabel("X scroll:"))
            b.addWidget(self.inputValues[0])
            self.inputValues[0].setText(str(newAction.args["dx"]))
            self.inputValues[0].show()
            layoutToAdd.addLayout(b)
            c = QHBoxLayout()
            c.addWidget(QLabel("Y scroll:"))
            c.addWidget(self.inputValues[1])
            self.inputValues[1].setText(str(newAction.args["dy"]))
            self.inputValues[1].show()
            layoutToAdd.addLayout(c)
            self.changeTable(newAction.actionStr, f"{newAction.args['dy']}, {newAction.args['dy']}")
        elif newCommand == "random" or newCommand == "sleep":
            if self.action.actionStr == "random" or self.action.actionStr == "sleep":
                value = self.action.args["value"]
                if self.oldArgs is None or self.oldArgs["value"] == value:
                    try:
                        value = float(self.inputValues[0].text())
                    except ValueError:
                        pass
                newAction = action(newCommand, args={
                    "value": value
                })
            else:
                newAction = action(newCommand, args={
                    "value": 0
                })
            b = QHBoxLayout()
            b.addWidget(QLabel("How much:"))
            layoutToAdd.addWidget(self.inputValues[0])
            self.inputValues[0].setText(str(newAction.args["value"]))
            layoutToAdd.addLayout(b)
            self.changeTable(newAction.actionStr, str(newAction.args["value"]))
        elif newCommand == "moveMouse":
            if self.action.actionStr == "moveMouse":
                xOutput = self.action.args["x"]
                yOutput = self.action.args["y"]
                timeOutput = self.action.args["time"]
                if self.oldArgs is None or (self.oldArgs["x"] == xOutput and self.oldArgs["y"] == yOutput and self.oldArgs["time"] == timeOutput):
                    # Check if a string is a float
                    try:
                        xOutput = float(self.inputValues[0].text())
                    except ValueError:
                        pass
                    try:
                        yOutput = float(self.inputValues[1].text())
                    except ValueError:
                        pass
                    try:
                        timeOutput = float(self.inputValues[2].text())
                    except ValueError:
                        pass
                newAction = action(newCommand, args={
                    "x": xOutput,
                    "y": yOutput,
                    "time": timeOutput
                })
            else:
                newAction = action(newCommand, args={
                    "x": 0,
                    "y": 0,
                    "time": 0
                })
            b = QHBoxLayout()
            b.addWidget(QLabel("X:"))
            b.addWidget(self.inputValues[0])
            self.inputValues[0].setText(str(newAction.args["x"]))
            layoutToAdd.addLayout(b)
            c = QHBoxLayout()
            c.addWidget(QLabel("Y:"))
            c.addWidget(self.inputValues[1])
            self.inputValues[1].setText(str(newAction.args["y"]))
            d = QHBoxLayout()
            d.addWidget(QLabel("Time:"))
            d.addWidget(self.inputValues[2])
            self.inputValues[2].setText(str(newAction.args["time"]))
            layoutToAdd.addLayout(c)
            layoutToAdd.addLayout(d)
            for i in range(3):
                self.inputValues[i].show()
            self.changeTable(newAction.actionStr,
                             f"{newAction.args['x']}, {newAction.args['y']}, {newAction.args['time']}")


        if self.comment is not None:
            newAction.comment = self.comment

        # Update every variables with the new data
        self.displayText.actions[self.displayText.actions.index(self.action)] = newAction
        self.action = newAction
        self.currentAction = self.action.actionStr
        # Needed for checking in the next cycle if
        self.oldArgs = self.action.args

        # Update the layout
        clear_layout(self.argoumentsInputs)
        if layoutToAdd is not None:
            self.argoumentsInputs.addLayout(layoutToAdd)
        self.oldIndex = index

    # Just for not having a lot of duplicated lines
    def changeTable(self, command, argouments):
        # isEditing to True so that we dont enter in a loop with on_combo_box_changed
        self.isEditing = True
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 1,
                                         QTableWidgetItem(command))
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                         QTableWidgetItem(argouments))
        self.isEditing = False

    # Sync the window with the table, and also validate the data
    def save(self):
        # Save the comment
        comment: str = self.inputValues[-1].text()
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 3,
                                         QTableWidgetItem(comment))
        self.displayText.actions[self.displayText.actions.index(self.action)].comment = comment

        # Save the command and the arguments
        currentCommand = self.select_combo.currentText()

        self.actionManager.saveString(self.displayText, self.father.parent.table, self.inputValues, self.action)

        if currentCommand == "moveMouse":
            x = self.inputValues[0].text()
            y = self.inputValues[1].text()
            time = self.inputValues[2].text()
            try:
                x = float(x)
                y = float(y)
                time = float(time)
            except ValueError:
                QMessageBox.about(self, "Error", "X and Y must be numbers")
                return
            self.displayText.actions[self.displayText.actions.index(self.action)].args["x"] = x
            self.displayText.actions[self.displayText.actions.index(self.action)].args["y"] = y
            self.displayText.actions[self.displayText.actions.index(self.action)].args["time"] = time
            self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                             QTableWidgetItem(str(x) + ", " + str(y) + ", " + str(time)))
        elif currentCommand == "scroll":
            dx = self.inputValues[0].text()
            dy = self.inputValues[1].text()
            try:
                dx = float(dx)
                dy = float(dy)
            except ValueError:
                QMessageBox.about(self, "Error", "X and Y must be numbers")
                return
            self.displayText.actions[self.displayText.actions.index(self.action)].args["dx"] = dx
            self.displayText.actions[self.displayText.actions.index(self.action)].args["dy"] = dy
            self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                             QTableWidgetItem(str(dx) + ", " + str(dy)))
        elif currentCommand == "sleep" or currentCommand == "random":
            value = self.inputValues[0].text()
            try:
                value = float(value)
            except ValueError:
                QMessageBox.about(self, "Error", "Value must be a number")
                return
            self.displayText.actions[self.displayText.actions.index(self.action)].args["value"] = value
            self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                             QTableWidgetItem(str(value)))
        # No else because we dont want to save on the table invalid states

    # Graceful shutdown
    def closeEvent(self, event):
        self.father.removeWindow(self)
        super().closeEvent(event)
