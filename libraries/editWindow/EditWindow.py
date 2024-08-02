from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QMessageBox, \
    QTableWidgetItem

from libraries.dynamicActions.action.ActionManager import actionManager
from libraries.editWindow.DisplayText import displayText


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

    def isAction(self, item):
        return self.action == item

    # This function is called by the table when a row gets updated, is needed for the sync
    def onItemEdit(self, item):
        if self.isAction(item) and not self.isEditing:
            self.updateLayout()

    def updateLayout(self):
        action, args, comment = self.action.getValues()

        # Every items in the select box
        # TODO make this list more accessible to everyon
        items = self.actionManager.getActionsStr()
        if action not in items:
            items.append(action)

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
        index = self.displayText.actions.index(self.action)
        layoutToAdd, newAction = self.actionManager.parseWindow(self.inputValues, self.action, self.oldArgs, newCommand,
                                                                self.select_combo, self.changeTable, newCommand,
                                                                layoutToAdd)


        if self.comment is not None:
            newAction.comment = self.comment

        # Update every libraries with the new data
        self.displayText.actions[index] = newAction
        self.action = newAction
        self.currentAction = self.action.getActionstr()
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
        idx = self.displayText.actions.index(self.action)
        self.father.parent.table.setItem(idx, 1,
                                         QTableWidgetItem(command))
        self.father.parent.table.setItem(idx, 2,
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



    # Graceful shutdown
    def closeEvent(self, event):
        self.father.removeWindow(self)
        super().closeEvent(event)
