from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton
from variables.DisplayText import displayText
from variables import actions


class editWindow(QMainWindow):
    def __init__(self, a, b):
        super().__init__()
        self.setWindowTitle("New Window")

        # Label with select box
        select_label = QLabel("Select:")
        self.select_combo = QComboBox()
        self.select_combo.addItems(["ciao", "test"])

        # Labels with input boxes
        label1 = QLabel("Label 1:")
        self.input1 = QLineEdit()

        label2 = QLabel("Label 2:")
        self.input2 = QLineEdit()

        # Label with input box for comments
        comment_label = QLabel("Comments:")
        self.comment_input = QLineEdit()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(select_label)
        layout.addWidget(self.select_combo)
        layout.addWidget(label1)
        layout.addWidget(self.input1)
        layout.addWidget(label2)
        layout.addWidget(self.input2)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_input)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
