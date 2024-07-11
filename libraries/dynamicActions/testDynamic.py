from libraries.dynamicActions.action import ActionManager


def main():
    actionManager = ActionManager.actionManager()
    actionManager.parseLine("write(l\\)ol) #ciao")


if __name__ == '__main__':
    main()
