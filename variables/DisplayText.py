from variables.RunnableMacro import runnableMacro


class displayText:
    def __init__(self, layout):
        super().__init__()
        self.actions = []
        self.layout = layout
        self.keybind = None

    def getString(self):
        output = ""
        lastRandom = 0
        if self.keybind is not None:
            output += f"keybind({self.keybind.char})\n"
        # TODO we are loosing random value here
        for action in self.actions:
            if action.random != lastRandom:
                lastRandom = action.random
                output += f"random({lastRandom})\n"
            output += action.__str__() + "\n"
        return output

    def setString(self, text):
        macro = runnableMacro()
        macro.loadScript(text)
        self.keybind = macro.keybind
        self.actions = macro.script
