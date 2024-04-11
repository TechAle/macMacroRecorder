from PyQt5 import Qt

from PyQt5.QtCore import Qt as tableQt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QSizePolicy, QScrollArea, QTableWidget, \
    QTableWidgetItem, QHeaderView, QMenu

from variables.DisplayText import displayText


class TableWidget(QTableWidget):
    def __init__(self, columns, rows):
        super().__init__(columns, rows)
        self.setContextMenuPolicy(tableQt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        action = menu.addAction("Edit")
        action.triggered.connect(lambda idx, pos_args=pos: self.print_row_index(idx, pos_args))
        menu.exec_(self.mapToGlobal(pos))

    def print_row_index(self, idx, pos):
        print(f"Row index: {idx} {pos}")
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

    def toPlainText(self):
        return self.displayText.getString()

    def setPlainText(self, text):
        self.displayText.setString(text)
