from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QSizePolicy, QScrollArea, QTableWidget, \
    QTableWidgetItem, QHeaderView

from variables.DisplayText import displayText


class displayAction(QWidget):


    def __init__(self):
        super().__init__()
        # Set the size policy of the widget to expanding
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create table
        self.table = QTableWidget(5, 4)  # 5 rows, 4 columns

        # Set column names
        self.table.setHorizontalHeaderLabels(["a", "b", "c", "d"])

        header = self.table.horizontalHeader()
        header.setMaximumSectionSize(400)
        self.table.setColumnWidth(0, 100)
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        # Create layout and add table
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.displayText = displayText(self.table)

    def toPlainText(self):
        return self.displayText.getString()

    def setPlainText(self, text):
        self.displayText.setString(text)
