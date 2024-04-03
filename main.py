import tkinter as tk
import os
import threading
import time
import random as rd
import threading
import time
from actions import action

import macmouse
from pynput.keyboard import Listener
from pynput.keyboard import Controller


class CircleColorChangerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Macro Manager")
        self.master.geometry("300x400")
        self.controller = Controller()

        self.keybind = None
        self.run = False
        self.actions = []

        # Check if "macros" directory exists, create it if it doesn't
        if not os.path.exists("macros"):
            os.makedirs("macros")

        # Create a button to update macros
        self.update_button = tk.Button(self.master, text="Update", command=self.update_macros)
        self.update_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a button to toggle circle color
        self.toggle_button = tk.Button(self.master, text="Toggle", command=self.toggle_circle_color)
        self.toggle_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a button to save the file
        self.save_button = tk.Button(self.master, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a frame to contain the text widget with border
        self.text_frame = tk.Frame(self.master, bd=1, relief=tk.SOLID)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Create a text widget for editing
        self.text = tk.Text(self.text_frame, height=10)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Variable to store text content
        self.text_content = tk.StringVar()
        self.text_content.set(self.text.get("1.0", tk.END))  # Initialize with initial content
        self.text.bind("<KeyRelease>", self.update_text_content)  # Bind key release event

        # Create a canvas widget
        self.canvas = tk.Canvas(self.master, width=200, height=150)
        self.canvas.pack()

        # Create a status at the bottom with a red circle at its left
        self.status_frame = tk.Frame(self.master)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(self.status_frame, text="Status", bg="lightgray")
        self.status_label.pack(side=tk.LEFT)

        self.circle_label = tk.Label(self.status_frame, text="●", fg="red", font=("Arial", 12))
        self.circle_label.pack(side=tk.LEFT)

        self.circle_color = "red"
        self.current_file = None

        self.update_macros()  # Call update_macros initially after packing circle_label

        listener = Listener(on_press=self.onPress)
        listener.start()

    def onPress(self, key):
        if self.keybind is None or self.circle_color == "red":
            return
        try:
           if key.char == self.keybind:
               self.run = not self.run
               self.idx = 0
        except Exception as ignored:
            pass

    def toggle_circle_color(self):
        self.run = False
        self.idx = 0
        if self.circle_color == "red":
            self.circle_label.config(fg="green")
            self.circle_color = "green"
        else:
            self.circle_label.config(fg="red")
            self.circle_color = "red"

    def update_macros(self):
        # Clear canvas before updating buttons
        for button in self.canvas.winfo_children():
            button.destroy()

        # Get list of files in "macros" directory
        macro_files = os.listdir("macros")

        # Create a button for each file in the "macros" directory
        for file_name in macro_files:
            # Remove file extension if present
            button_text = os.path.splitext(file_name)[0]
            button = tk.Button(self.canvas, text=button_text,
                               command=lambda name=file_name: self.load_file_content(name))
            button.pack()

        # Schedule the next update
        self.master.after(5000, self.update_macros)  # Update every 5 seconds

    def load_file_content(self, file_name):
        if self.circle_color != "red":
            self.toggle_circle_color()
        # Save content to the previous file
        if self.current_file:
            file_path = os.path.join("macros", self.current_file)
            with open(file_path, "w") as file:
                content = self.text.get("1.0", tk.END)
                file.write(content)

        # Load content from the clicked file
        file_path = os.path.join("macros", file_name)
        with open(file_path, "r") as file:
            content = file.read()
        self.text.delete("1.0", tk.END)  # Clear previous content
        self.text.insert(tk.END, content)

        self.current_file = file_name
        self.update_text_content()
        self.prepareActions()

    def save_file(self):
        if self.circle_color != "red":
            self.toggle_circle_color()
        if self.current_file:
            file_path = os.path.join("macros", self.current_file)
            with open(file_path, "w") as file:
                content = self.text.get("1.0", tk.END)
                file.write(content)
        self.prepareActions()

    def prepareActions(self):
        self.actions = []
        self.idx = 0
        content = self.text_content.get()
        if (content := content.split("\n")).__len__() > 0:
            b = 0
            self.keybind = content[0].split(":")[1].strip()
            self.random = float(content[1].split("(")[1][:-1])
            for i in range(2, content.__len__()):
                self.actions.append(action(content[i], self.random, self.controller))


    def main(self):
        # Create a thread to run the infinite loop
        thread = threading.Thread(target=self.infinite_loop)
        thread.daemon = True  # Daemonize the thread to stop it with the main application
        thread.start()

        # Start the Tkinter main loop
        self.master.mainloop()

    def infinite_loop(self):
        # Infinite loop
        while True:
            if not self.run:
                time.sleep(0.2)
                continue
            if self.actions[self.idx].run():
                self.run = False
            self.idx += 1
            if self.idx == self.actions.__len__():
                self.idx = 0

    def update_text_content(self, event=None):
        new_text = self.text.get("1.0", tk.END)
        self.text_content.set(new_text)
        print("New text:", new_text.strip())



if __name__ == "__main__":
    root = tk.Tk()
    app = CircleColorChangerApp(root)
    app.main()
