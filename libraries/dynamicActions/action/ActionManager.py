import importlib
import inspect
import os

from libraries.dynamicActions.action.ActionLol import actionLol


class actionManager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.actionsInstancer: {str: actionLol} = {}
        self.actions: [actionLol] = []
        self.keybind = None
        self.loadActions()
        self.currentRunning = None

    def setCurrentRunning(self, obj):
        self.currentRunning = obj

    def parseLine(self, line: str) -> str:
        command = line.split('(')
        extra = '('.join(command[1:])
        command = command[0]
        if command == "keybind":
            output, _ = self.actionsInstancer[command].parseLine(extra)
            if type(output) == str:
                return "keybind: " + output
            return "Error parsing keybind"
        elif self.actionsInstancer.__contains__(command):
            argouments, comment = self.actionsInstancer[command].parseLine(extra)
            if type(argouments) != bool:
                action, error = self.actionsInstancer[command].createAction(argouments, comment)
                self.actions.append(action)
                return ""
            else:
                argouments, comment = self.actionsInstancer["invalid"].parseLine(extra)
                action, error = self.actionsInstancer["invalid"].createAction(argouments, comment)
                action.setCustomAction(command)
                self.actions.append(action)
                return "Uknown action"
        else:
            argouments, comment = self.actionsInstancer["invalid"].parseLine(extra)
            action, error = self.actionsInstancer["invalid"].createAction(argouments, comment)
            action.setCustomAction(command)
            self.actions.append(action)
            return "Uknown action"

    def parseWindow(self, inputValues, actionValue, oldArgs, command, select_combo, table, newCommand, layoutToAdd):
        if self.actionsInstancer.__contains__(command):
            return self.actionsInstancer[command].editWindow(inputValues, actionValue, oldArgs, select_combo, table,
                                                               newCommand, layoutToAdd)
        else:
            return self.actionsInstancer["invalid"].editWindow(inputValues, actionValue, oldArgs, select_combo, table,
                                                                 newCommand, layoutToAdd)

    def actionExists(self, action: str) -> bool:
        return self.actionsInstancer.__contains__(action)

    def getActionsStr(self) -> [str]:
        output = [x for x in self.actionsInstancer if x != "keybind"]
        return output

    def loadActions(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions/")
        for file_name in os.listdir(directory):
            if file_name.endswith('.py'):
                modules = importlib.import_module('.'.join(__name__.split(".")[0:-1]) + ".actions." + file_name[:-3])
                for name, obj in inspect.getmembers(modules):
                    if inspect.isclass(obj) and issubclass(obj, actionLol) and type(obj) != actionLol and len(obj.actionStr) > 0:
                        self.actionsInstancer[obj.actionStr] = obj

    def saveString(self, displayText, table, inputValues, action):
        if self.actionsInstancer.__contains__(action.actionStr):
            self.actionsInstancer[action.actionStr].save(displayText, table, inputValues, action)
        else:
            self.actionsInstancer["invalid"].save(displayText, table, inputValues, action)

    def onCellEdit(self, action, newArgs, actionChange):
        if self.actionsInstancer.__contains__(action):
            return self.actionsInstancer[action].editTable(newArgs, actionChange)
        else:
            return self.actionsInstancer["invalid"].editTable(newArgs, actionChange)

    def getSvg(self, action):
        if self.actionsInstancer.__contains__(action):
            return self.actionsInstancer[action].getSvg()
        else:
            return self.actionsInstancer["invalid"].getSvg()
