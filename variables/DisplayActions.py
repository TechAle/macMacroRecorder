from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QSizePolicy


class displayAction(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.text = QTextEdit("")
        layout.addWidget(self.text)

    def toPlainText(self):
        return self.text.toPlainText()

    def setPlainText(self, text):
        self.text.setPlainText(text)
