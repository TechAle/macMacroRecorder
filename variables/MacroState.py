class macroState:
    DISABLED = 0 # When toggle is off
    WAITING = 1 # When toggle is on but we are waiting for the keybind
    RUNNING = 2 # When toggle is on and the macro is running
