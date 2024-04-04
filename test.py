import sys
import os
from functools import partial

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QInputDialog
from PyQt5.uic.properties import QtGui


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt Program with Navigation Bar and Footer')
        self.setGeometry(100, 100, 400, 300)

        # Create macros directory if it doesn't exist
        if not os.path.exists("macros"):
            os.makedirs("macros")

        # Navigation Bar
        self.navbar_layout = QHBoxLayout()
        self.navbar_label = QLabel('Scripts available:', self)
        self.navbar_label.setStyleSheet("font-weight: bold;")
        self.navbar_layout.addWidget(self.navbar_label)

        # Script Buttons Layout
        self.script_buttons_layout = QVBoxLayout()

        # Text Field
        self.text_field = QTextEdit(self)  # Use QTextEdit for multiline text input
        self.text_field.setFixedHeight(100)  # Set the height of the text field

        # Footer
        footer_layout = QHBoxLayout()
        button_save = QPushButton('Save', self)
        self.button_update = QPushButton('Update', self)
        self.button_new = QPushButton('New', self)  # New button
        button_save.clicked.connect(self.saveClicked)
        self.button_update.clicked.connect(self.updateClicked)
        self.button_new.clicked.connect(self.newButtonClicked)  # Connect to newButtonClicked method
        footer_layout.addWidget(button_save)
        footer_layout.addWidget(self.button_update)
        footer_layout.addWidget(self.button_new)

        # Toggle button layout
        toggle_layout = QHBoxLayout()
        self.button_toggle = QPushButton('Toggle', self)  # Keep a reference to the button
        self.button_toggle.clicked.connect(self.toggleClicked)  # Connect to toggleClicked method
        toggle_layout.addWidget(self.button_toggle)
        self.button_start_recording = QPushButton('Start Recording', self)
        toggle_layout.addWidget(self.button_start_recording)
        self.button_stop_recording = QPushButton('Start Recording', self)
        toggle_layout.addWidget(self.button_stop_recording)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.navbar_layout)
        main_layout.addLayout(self.script_buttons_layout)  # Add script buttons layout
        main_layout.addWidget(self.text_field)
        main_layout.addLayout(footer_layout)
        main_layout.addLayout(toggle_layout)  # Add toggle button layout

        self.setLayout(main_layout)




        # Update buttons initially
        self.updateButtons()

    def saveClicked(self):
        print("Save button clicked.")

    def toggleClicked(self):
        if self.button_toggle.palette().color(self.button_toggle.backgroundRole()).name() == '#008000':
            self.button_toggle.setStyleSheet("background-color: red;")
        else:
            self.button_toggle.setStyleSheet("background-color: green;")

    def updateClicked(self):
        self.updateButtons()

    def newButtonClicked(self):
        # Prompt the user for a new file name
        new_file_name, ok = QInputDialog.getText(self, 'New File', 'Enter the name for the new file:')
        if ok and new_file_name:
            # Check if the file already exists
            if os.path.exists(os.path.join("macros", new_file_name)):
                QMessageBox.warning(self, 'File Exists', 'A file with the same name already exists.')
            else:
                # Create the new file
                with open(os.path.join("macros", new_file_name), 'w') as f:
                    f.write("")
                QMessageBox.information(self, 'File Created', f'New file "{new_file_name}" created successfully.')
                # Update buttons after creating new file
                self.updateButtons()

    def updateButtons(self):
        # Clear existing buttons in the script buttons layout
        for i in reversed(range(self.script_buttons_layout.count())):
            widget = self.script_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # List files in the "macros" folder, ignoring files starting with "."
        macro_files = [file for file in os.listdir("macros") if not file.startswith('.')]

        # Add buttons for each file to the script buttons layout
        for file in macro_files:
            button = QPushButton(file, self)
            button.clicked.connect(partial(self.loadFileContent, file))  # Connect button to loadFileContent method
            self.script_buttons_layout.addWidget(button)

    def loadFileContent(self, file):
        with open(os.path.join("macros", file), 'r') as f:
            content = f.read()
            self.text_field.setPlainText(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
