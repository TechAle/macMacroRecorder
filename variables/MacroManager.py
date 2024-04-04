from variables.RunnableMacro import runnableMacro


class macroManager():

    def __init__(self):
        self.scripts = {}

    def onDrag(self, point):
        pass

    def onToggle(self, script) -> bool:
        return self.scripts[script].toggle()

    def onCreate(self, script):
        if not self.scripts.keys().__contains__(script):
            self.scripts[script] = runnableMacro()
        return self.scripts[script].running

    def removeScript(self, script):
        if self.scripts.keys().__contains__(script):
            if not self.scripts[script].running:
                self.scripts.pop(script)

    def isEnabled(self, script):
        if self.scripts.keys().__contains__(script):
            return self.scripts[script].running
        else:
            return None

    def onPress(self, key):
        pass