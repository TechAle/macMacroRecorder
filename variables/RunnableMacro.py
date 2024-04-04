import threading


class runnableMacro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        # TODO get keybind from the file
        # TODO get script from the file

    def toggle(self):
        self.running = not self.running
        return self.running


    def run(self):
        pass