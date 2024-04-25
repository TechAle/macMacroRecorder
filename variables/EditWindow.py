import importlib

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QMessageBox, \
    QTableWidgetItem

from variables.DisplayText import displayText
from variables import actions
from variables.actions import action


class editWindow(QMainWindow):

    def __init__(self, displayText: displayText, action, father):
        super().__init__()
        self.setWindowTitle("New Window")
        self.displayText: displayText = displayText
        self.action = action
        self.father = father

        # Label with select box
        select_label = QLabel("Select:")
        self.firstLoad = True
        self.select_combo = QComboBox()
        self.select_combo.currentIndexChanged.connect(self.on_combo_box_changed)
        # Set active selection "test"
        # Check when select_combo changes

        # Labels with input boxes
        self.argoumentsInputs = QVBoxLayout()

        # Label with input box for comments
        comment_label = QLabel("Comments:")
        self.comment_input = QLineEdit()

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
                "value": ""
            })
            layoutToAdd.addWidget(QLabel("What to write:"))
            layoutToAdd.addWidget(QLineEdit())
        elif ["left", "rightClick", "middleClick"].__contains__(newCommand):
            newAction = action(newCommand)
        elif newCommand == "scroll":
            newAction = action(newCommand, args={
                "dx": 0,
                "dy": 0
            })
            layoutToAdd.addWidget(QLabel("X scroll:"))
            layoutToAdd.addWidget(QLineEdit())
            layoutToAdd.addWidget(QLabel("Y scroll:"))
            layoutToAdd.addWidget(QLineEdit())
        elif newCommand == "random" or newCommand == "sleep":
            newAction = action(newCommand, args={
                "value": 0
            })
            layoutToAdd.addWidget(QLabel("How much:"))
            layoutToAdd.addWidget(QLineEdit())
        elif newCommand == "moveMouse":
            newAction = action(newCommand, args={
                "x": 0,
                "y": 0,
                "time": 0
            })
            layoutToAdd.addWidget(QLabel("X:"))
            layoutToAdd.addWidget(QLineEdit())
            layoutToAdd.addWidget(QLabel("Y:"))
            layoutToAdd.addWidget(QLineEdit())
            layoutToAdd.addWidget(QLabel("Time:"))
            layoutToAdd.addWidget(QLineEdit())
        else:
            newAction = action(newCommand)

        self.father.parent.table.setItem(self.displayText.actions.index(self.action), 1,
                                         QTableWidgetItem(newAction.actionStr))
        self.displayText.actions[self.displayText.actions.index(self.action)] = newAction
        self.action = newAction
        for i in reversed(range(self.argoumentsInputs.count())):
            item = self.argoumentsInputs.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.argoumentsInputs.removeItem(item)
        self.argoumentsInputs.addLayout(layoutToAdd)

    def save(self):
        pass

    def closeEvent(self, event):
        self.father.removeWindow(self)
        super().closeEvent(event)
