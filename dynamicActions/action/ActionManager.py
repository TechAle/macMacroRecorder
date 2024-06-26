import importlib
import inspect
import os

from dynamicActions.action.ActionLol import actionLol


class actionManager:
    def __init__(self):
        self.actionsInstancer: {str: actionLol} = {}
        self.actions: [actionLol] = []
        self.loadActions()

    def parseLine(self, line: str) -> str:
        command = line.split('(')
        extra = '('.join(command[1:])
        command = command[0]
        if command == "keybind":
            output, _ = self.actionsInstancer[command].parseLine(extra)
            if type(output) == str:
                return "keybind: " + output
        elif self.actionsInstancer.__contains__(command):
            argouments, comment = self.actionsInstancer[command].parseLine(extra)
            if type(argouments) == str:
                action, error = self.actionsInstancer[command].createAction(argouments, comment)
                self.actions.append(action)
                return ""
            else:
                # Error message
                return "Error parsing"
        return "Uknown action"

    def parseWindow(self, inputValues, changeWindow, action, oldArgs, command, select_combo):
        pass

    def actionExists(self, action: str) -> bool:
        return self.actionsInstancer.__contains__(action)

    def loadActions(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions/")
        for file_name in os.listdir(directory):
            if file_name.endswith('.py'):
                modules = importlib.import_module('.'.join(__name__.split(".")[0:-1]) + ".actions." + file_name[:-3])
                for name, obj in inspect.getmembers(modules):
                    if inspect.isclass(obj) and issubclass(obj, actionLol) and type(obj) != actionLol:
                        self.actionsInstancer[obj.actionStr] = obj
