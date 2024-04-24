import importlib

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton

from variables.DisplayText import displayText
from variables import actions


class editWindow(QMainWindow):

    def __init__(self, displayText: displayText, action, father):
        super().__init__()
        self.setWindowTitle("New Window")
        self.displayText: displayText = displayText
        self.action = action
        self.father = father

        # Label with select box
        select_label = QLabel("Select:")
        self.select_combo = QComboBox()
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
        if action.actionStr not in items:
            items.append(action.actionStr)

        self.select_combo.addItems(items)
        self.select_combo.setCurrentIndex(items.index(action.actionStr))
        self.select_combo.currentIndexChanged.connect(self.on_combo_box_changed)
        # Set active selection "test"
        # Check when select_combo changes


        # Labels with input boxes
        label1 = QLabel("Argouments:")
        self.input1 = QLineEdit()
        self.input1.setText(str(action.args))

        # Label with input box for comments
        comment_label = QLabel("Comments:")
        self.comment_input = QLineEdit()
        self.comment_input.setText(action.comment)

        # Add a save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(select_label)
        layout.addWidget(self.select_combo)
        layout.addWidget(label1)
        layout.addWidget(self.input1)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_input)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_combo_box_changed(self, index):
        print("Selected index:", index)
        print("Selected text:", self.select_combo.currentText())


    def save(self):
        print("Save")
    def closeEvent(self, event):
        self.father.removeWindow(self)
        super().closeEvent(event)
