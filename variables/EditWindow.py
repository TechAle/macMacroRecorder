import importlib

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QMessageBox, \
    QTableWidgetItem, QHBoxLayout

from variables.DisplayText import displayText
from variables import actions
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
        # I think i will never need more then 10 QLineEdit
        self.inputValues: [QLineEdit] = [QLineEdit() for x in range(10)]

        # Label with select box
        select_label = QLabel("Select:")
        self.firstLoad = True
        self.isEditing = False
        self.select_combo = QComboBox()
        self.select_combo.currentIndexChanged.connect(self.on_combo_box_changed)
        # Set active selection "test"
        # Check when select_combo changes

        # Labels with input boxes
        self.argoumentsInputs = QVBoxLayout()

        # Label with input box for comments
        comment_label = QLabel("Comments:")
        self.comment_input = self.inputValues[-1]

        # Add a save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(select_label)
        layout.addWidget(self.select_combo)
        # Add argoumentsInput
        layout.addLayout(self.argoumentsInputs)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_input)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.update_args()
        self.setCentralWidget(central_widget)

    def onItemEdit(self, item: action):
        if self.action == item and not self.isEditing:
            self.update_args()

    def update_args(self):
        action, args, comment = self.action.getValues()
        items = ["sleep",
                 "rightClick",
                 "leftClick",
                 "shift",
                 "scroll",
                 "unshift",
                 "middleClick",
                 "stop",
                 "type",
                 "write",
                 "moveMouse"]
        if action not in items:
            items.append(action)

        self.select_combo.clear()
        self.select_combo.addItems(items)
        self.select_combo.setCurrentIndex(items.index(action))

        self.comment_input.setText(comment)

    def on_combo_box_changed(self, index):
        if self.firstLoad:
            self.firstLoad = False
            return
        print("Selected index:", index)
        print("Selected text:", self.select_combo.currentText())
        layoutToAdd = QVBoxLayout()
        # Clear everything in the layout
        # TODO edit keybind
        newCommand = self.select_combo.currentText()
        if newCommand == "write" or newCommand == "type":
            newAction = action(newCommand, args={
                "value": "" if self.action.actionStr != "write" and self.action.actionStr != "type" else self.action.args["value"]
            })
            b = QHBoxLayout()
            b.addWidget(QLabel("What to write:"))
            b.addWidget(self.inputValues[0])
            self.inputValues[0].setText(str(newAction.args["value"]))
            self.inputValues[0].show()
            layoutToAdd.addLayout(b)
            self.changeTable(newAction.actionStr, str(newAction.args['value']))
        elif ["left", "rightClick", "middleClick"].__contains__(newCommand):
            newAction = action(newCommand)
            self.changeTable(newAction.actionStr, "")
        elif newCommand == "scroll":
            newAction = action(newCommand, args={
                "dx": 0 if self.action.actionStr != "scroll" else self.action.args["dx"],
                "dy": 0 if self.action.actionStr != "scroll" else self.action.args["dy"]
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
            self.changeTable(newAction.actionStr, f"{newAction.args['xy']}, {newAction.args['dy']}")
        elif newCommand == "random" or newCommand == "sleep":
            newAction = action(newCommand, args={
                "value": 0 if self.action.actionStr != "random" and self.action.actionStr != "sleep" else self.action.args["value"]
            })
            b = QHBoxLayout()
            b.addWidget(QLabel("How much:"))
            layoutToAdd.addWidget(self.inputValues[0])
            self.inputValues[0].setText(str(newAction.args["value"]))
            layoutToAdd.addLayout(b)
            self.changeTable(newAction.actionStr, str(newAction.args["value"]))
        elif newCommand == "moveMouse":
            newAction = action(newCommand, args={
                "x": 0 if self.action.actionStr != "moveMouse" else self.action.args["x"],
                "y": 0 if self.action.actionStr != "moveMouse" else self.action.args["y"],
                "time": 0 if self.action.actionStr != "moveMouse" else self.action.args["time"]
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
            self.changeTable(newAction.actionStr, f"{newAction.args['x']}, {newAction.args['y']}, {newAction.args['time']}")
        else:
            newAction = action(newCommand)
            self.changeTable(newAction.actionStr, "")
        self.displayText.actions[self.displayText.actions.index(self.action)] = newAction
        self.action = newAction
        self.currentAction = self.action.actionStr
        clear_layout(self.argoumentsInputs)
        self.argoumentsInputs.addLayout(layoutToAdd)

    def changeTable(self, command, argouments):
        self.isEditing = True
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 1,
                                         QTableWidgetItem(command))
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                         QTableWidgetItem(argouments))
        self.isEditing = False

    def save(self):
        # Save the comment
        comment: str = self.inputValues[-1].text()
        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 3,
                                         QTableWidgetItem(comment))
        self.displayText.actions[self.displayText.actions.index(self.action)].comment = comment
        # Now save the argouments
        currentCommand = self.select_combo.currentText()
        if currentCommand == "write" or currentCommand == "type":
            self.displayText.actions[self.displayText.actions.index(self.action)].args["value"] = \
                self.inputValues[0].text()
            self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                             QTableWidgetItem(self.inputValues[0].text()))
        elif currentCommand == "moveMouse":
            x = self.inputValues[0].text()
            y = self.inputValues[1].text()
            time = self.inputValues[2].text()
            # Check if x and y are floats
            try:
                x = float(x)
                y= float(y)
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
            # Check if x and y are floats
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
            # Check if x and y are floats
            try:
                value = float(value)
            except ValueError:
                QMessageBox.about(self, "Error", "Value must be a number")
                return
            self.displayText.actions[self.displayText.actions.index(self.action)].args["value"] = value
            self.father.parent.table.setItem(self.displayText.actions.index(self.action), 2,
                                             QTableWidgetItem(str(value)))


    def closeEvent(self, event):
        self.father.removeWindow(self)
        super().closeEvent(event)
