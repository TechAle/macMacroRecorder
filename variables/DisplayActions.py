from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QSizePolicy, QScrollArea

from variables.DisplayText import displayText


class displayAction(QWidget):


    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.displayText = displayText(self.layout)


    def toPlainText(self):
        return self.displayText.getString()

    def setPlainText(self, text):
        self.displayText.setString(text)
