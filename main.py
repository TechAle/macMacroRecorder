import json
import os
import sys
import time
from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, \
    QMessageBox, QInputDialog
from pynput.keyboard import Listener as ListenerKeyboard, KeyCode
from pynput.mouse import Listener as ListenerMouse

from variables.MacroManager import macroManager
from variables.MacroState import macroState

import HIServices

if not HIServices.AXIsProcessTrusted():
    print("This process is NOT a trusted accessibility client, so pynput will not "
          "function properly. Please grant accessibility access for this app in "
          "System Preferences.")


class MyWindow(QWidget):
    signalHander = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initVariables()
        self.initUI()
        self.prepareListeners()
        self.prepareSignals()
        self.b = 0

    def prepareSignals(self):
        self.signalHander.connect(self.onSignal)

    def onSignal(self, data):
        if data == "askConfirmOverwrite":
            # Ask if they are sure they want to override the current file
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)

            msg.setText("Are you sure you want to override the current file?")
            msg.setInformativeText("This will erase all the content of the current file.")
            msg.setWindowTitle("Confirmation")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            retval = msg.exec_()
            if retval != QMessageBox.Yes:
                return
            self.macroManager.startRecording(self.lastSelected)
        elif data == "noLoaded":
            QMessageBox.information(self, "Feedback", "You have not loaded any file",
                                    QMessageBox.Abort)


    def prepareListeners(self):
        # Create a new thread with the
        listenerKeyboard = ListenerKeyboard(on_press=self.onPress)
        listenerKeyboard.start()
        # pyobject race condition fix, thanks lettow-humain you saved me from lots of hours of desperation
        listenerKeyboard.wait()
        listenerMouse = ListenerMouse(
            on_move=self.onMove,
            on_click=self.onClick,
            on_scroll=self.onScroll)
        listenerMouse.start()

    def onPress(self, key):
        if self.focus: # pyobject would crash without this
            return
        if key == self.configurations["keybindStart"]:
            self.startRecording()
        elif key == self.configurations["keybindStop"]:
            self.stopRecording()
        self.macroManager.onPress(key)

    def onMove(self, x, y):
        self.macroManager.onMove(x, y)

    def onClick(self, x, y, button, pressed):
        self.macroManager.onClick(x, y, button, pressed)

    def onScroll(self, x, y, dx, dy):
        self.macroManager.onScroll(x, y, dx, dy)

    def initVariables(self):
        self.lastSelected = None
        self.isRecording = False
        self.focus = False
        if os.path.exists("configurations.json"):
            with open("configurations.json", "r") as f:
                self.configurations = json.load(f)
                self.configurations["keybindStart"] = KeyCode.from_char(self.configurations["keybindStart"])
                self.configurations["keybindStop"] = KeyCode.from_char(self.configurations["keybindStop"])
                self.macroManager = macroManager(self.configurations["mouseDelay"])
        else:
            return self.initDefault()

    def initDefault(self):
        self.configurations = {
            "keybindStart": "",
            "keybindStop": ""
        }



    def save_configurations(self):
        with open("configurations.json", "w") as f:
            json.dump(self.configurations, f, indent=4)

    def initUI(self):
        self.setWindowTitle('PyQt Program with Navigation Bar and Footer')
        self.setGeometry(100, 100, 400, 300)

        # Create macros directory if it doesn't exist
        if not os.path.exists("macros"):
            os.makedirs("macros")

        # Navigation Bar
        self.navbar_layout = QHBoxLayout()
        self.text_running = QLabel('')
        self.navbar_label = QLabel('Scripts available:', self)
        self.navbar_label.setStyleSheet("font-weight: bold;")
        self.navbar_layout.addWidget(self.navbar_label)
        self.navbar_layout.addWidget(self.text_running)

        # Script Buttons Layout
        self.script_buttons_layout = QVBoxLayout()

        # Text Field
        self.text_field = QTextEdit(self)  # Use QTextEdit for multiline text input
        self.text_field.setFixedHeight(100)  # Set the height of the text field
        # Connect text_field to two functions when the user selects it
        self.text_field.installEventFilter(self)

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
        self.button_start_recording.clicked.connect(self.startRecording)
        toggle_layout.addWidget(self.button_start_recording)
        self.button_stop_recording = QPushButton('Stop Recording', self)
        self.button_stop_recording.clicked.connect(self.stopRecording)
        toggle_layout.addWidget(self.button_stop_recording)

        keybindLayout = QHBoxLayout()
        self.buttonKeybindStartRecording = QPushButton(
            "Keybind Start Recording: " + str(self.configurations["keybindStart"]))
        self.buttonKeybindStartRecording.clicked.connect(self.pressedKeybindStart)
        self.buttonKeybindStopRecording = QPushButton("Keybind Stop Recording: " + str(self.configurations["keybindStop"]))
        self.buttonKeybindStopRecording.clicked.connect(self.pressedKeybindStop)
        keybindLayout.addWidget(self.buttonKeybindStartRecording)
        keybindLayout.addWidget(self.buttonKeybindStopRecording)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.navbar_layout)
        main_layout.addLayout(self.script_buttons_layout)  # Add script buttons layout
        main_layout.addWidget(self.text_field)
        main_layout.addLayout(footer_layout)
        main_layout.addLayout(toggle_layout)  # Add toggle button layout
        main_layout.addLayout(keybindLayout)

        self.setLayout(main_layout)

        # Update buttons initially
        self.updateButtons()

    def eventFilter(self, obj, event):
        if obj == self.text_field:
            if event.type() == event.FocusIn:
                self.focus = True
            elif event.type() == event.FocusOut:
                self.focus = False
        return super().eventFilter(obj, event)

    def startRecording(self):
        if self.macroManager.isRecording:
            return
        if self.lastSelected is None:
            self.signalHander.emit("noLoaded")
            # Alert saying no file has been selected
            return
        if self.text_field.toPlainText() != "":
            self.signalHander.emit("askConfirmOverwrite")
            return
        self.macroManager.startRecording(self.lastSelected)

    def stopRecording(self):
        if not self.macroManager.isRecording:
            # Alert saying is not recording
            QMessageBox.information(self, "Recording", "You are not currently recording", QMessageBox.Abort)
            return
        output = self.macroManager.stopRecording()
        self.text_field.setPlainText(output)
        self.button_toggle.setStyleSheet("background-color: red;")


    def pressedKeybindStart(self):
        text, okPressed = QInputDialog.getText(self, "Get keybind start",
                                               "Enter the keybind for starting (1 character):", QLineEdit.Normal, "")
        if not okPressed:
            QMessageBox.information(self, "Feedback", "Cancelled successfully",
                                    QMessageBox.Ok)
        elif text == '' or len(text) != 1:
            QMessageBox.information(self, "Feedback", "The keybind must be 1 long",
                                    QMessageBox.Abort)
        else:
            self.configurations["keybindStart"] = text
            self.buttonKeybindStartRecording.setText("Keybind start recording: " + text)
            QMessageBox.information(self, "Feedback", "Keybind for starting a recording changed without any problems",
                                    QMessageBox.Ok)
            self.save_configurations()

    def pressedKeybindStop(self):
        text, okPressed = QInputDialog.getText(self, "Get keybind stop",
                                               "Enter the keybind for stopping (1 character):", QLineEdit.Normal, "")
        if not okPressed:
            QMessageBox.information(self, "Feedback", "Cancelled successfully",
                                    QMessageBox.Ok)
        elif text == '' or len(text) != 1:
            QMessageBox.information(self, "Feedback", "The keybind must be 1 long",
                                    QMessageBox.Abort)
        else:
            self.configurations["keybindStop"] = text
            self.buttonKeybindStopRecording.setText("Keybind stop recording: " + text)
            QMessageBox.information(self, "Feedback", "Keybind for stopping a recording changed without any problems",
                                    QMessageBox.Ok)
            self.save_configurations()

    def saveClicked(self):
        # update lastSelected file in macros/lastSelected
        with open(os.path.join("macros", self.lastSelected), 'w') as f:
            f.write(self.text_field.toPlainText())
        self.macroManager.update(self.lastSelected)

    def toggleClicked(self):
        if self.lastSelected is not None and (onToggle := self.macroManager.onToggle(self.lastSelected)) is not None:
            if onToggle == macroState.WAITING:
                self.button_toggle.setStyleSheet("background-color: green;")
            else:
                self.button_toggle.setStyleSheet("background-color: red;")
        else:
            self.button_toggle.setStyleSheet("")
            if not self.lastSelected:
                QMessageBox.information(self, "Feedback", "You have not loaded any file",
                                        QMessageBox.Abort)
            else:
                QMessageBox.information(self, "Feedback", "The file you loaded is not valid, please fix the errors and save",
                                        QMessageBox.Abort)

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
        if self.lastSelected is not None:
            with open(os.path.join("macros", self.lastSelected), "w") as f:
                f.write(self.text_field.toPlainText())
            self.macroManager.removeScript(self.lastSelected)
        with open(os.path.join("macros", file), 'r') as f:
            content = f.read()
            self.text_field.setPlainText(content)
        self.lastSelected = file
        if type(success := self.macroManager.onCreate(file)) != str:
            if success:
                self.button_toggle.setStyleSheet("background-color: green;")
            else:
                self.button_toggle.setStyleSheet("background-color: red;")
        else:
            self.button_toggle.setStyleSheet("")
            QMessageBox.information(self, "Feedback", success,
                                    QMessageBox.Abort)
        self.text_running.setText("Currently editing: " + file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
