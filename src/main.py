import pyautogui
import argparse
import threading
import keyboard
import json
import os, sys
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep

# Ensure we run from inside the _internal folder.
os.chdir(os.path.dirname(__file__))

if os.path.exists("../_internal"):
    DEV = False
else:
    DEV = True

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", help="The speed of the autoclicker.")
parser.add_argument("-k", "--hotkey", help="The toggle hotkey.")
parser.add_argument("-v", "--view", action="store_true", help="View current config.")
parser.add_argument("-c", "--clicker", action="store_true", help="Start the autoclicker.")
parser.add_argument("-g", "--gui", action="store_true", help="Start the autoclicker in GUI mode.")

args = parser.parse_args()

pyautogui.PAUSE = 0

class Clicker:
    def __init__(self, stringvar: tk.StringVar | None = None) -> None:
        """
        Main clicker class. Manages both hotkey checking and autoclicking.

        @label: (tkinter.StringVar/None) - A Tkinter StringVar to update with the status of the clicker.
        """
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        
        self.running = False
        self.statustext = stringvar
    
        self.__pressed = False

        # Create the hotkey thread.
        hotkey = threading.Thread(name="hotkey_loop", target=self.__hotkey_loop)
        hotkey.daemon = True
        hotkey.start()
    
    def trigger(self, state: bool):
        """
        Manually switch the clicker's state.

        Returns False and does nothing if the clicker was already in that state.
        Returns True otherwise.

        @state: (bool) - Whether or not the clicker should be running.
        """
        sleep(1)

        if state != self.running:
            if state:
                self.__start_autoclicker()
            else:
                self.__stop_autoclicker()
            return True

        print("Ignoring. Autoclicker was already in that state.")
        return False

    def __clicker_loop(self):
        while self.running:
            pyautogui.click()
            sleep(self.config["speed"])

    def __start_autoclicker(self):
        if self.statustext is not None:
            self.statustext.set(f"Running! ({config["hotkey"]})")
        
        self.running = True

        # Start the autoclicker.
        clicker = threading.Thread(name="clicker_loop", target=self.__clicker_loop)
        clicker.daemon = True
        clicker.start()
        print("Started autoclicker.")

    def __stop_autoclicker(self):
        if self.statustext is not None:
            self.statustext.set(f"Not Running. ({config["hotkey"]})")
        
        self.running = False
        print("Stopped autoclicker.")

    def __hotkey_loop(self):
        """ 
        Loop for checking pressed keys to see if it matches the user hotkeys.
        """

        while True:
            if keyboard.is_pressed(self.config["hotkey"]) and not self.__pressed:
                self.__pressed = True

            if self.__pressed:
                while True:
                    if not keyboard.is_pressed(self.config["hotkey"]):
                        self.__pressed = False
                        break
                    sleep(0.001)
                
                if self.running == True:
                    self.__stop_autoclicker()
                else:
                    self.__start_autoclicker()
            sleep(0.01)


def update_config(value: str, data):
    """
    Update a value in the config.

    @value: (str) - The value to update. Returns `False` if it does not exist.
    @data: - The data to update `value` with.
    """
    with open("./config.json", "r") as f:
        current_config: dict = json.load(f)

    current_value = current_config.get(value, None)

    # Value doesn't exist.
    if not current_value:
        return False

    current_config[value] = data

    with open("./config.json", "w") as f:
        json.dump(current_config, f, indent=2)

if not os.path.exists("./config.json"):
    with open("config.json", "w") as f:
        json.dump({"speed": 1, "hotkey": "ctrl+o"}, f)

if args.speed:
    if not float(args.speed) >= 0:
        print("Please supply a number greater than or equal to zero!!")
        sys.exit(1)

    update_config("speed", float(args.speed))
    print(f"The autoclicker speed is now {args.speed}.")
    sys.exit(0)
elif args.hotkey:
    hotkeys = args.hotkey.split("+")

    for key in hotkeys:
        if key not in pyautogui.KEYBOARD_KEYS:
            print(f"{key} is not a valid key!")
            print(f"Please choose a key in the following list: {", ".join(pyautogui.KEYBOARD_KEYS)}")
            sys.exit(1)

    print(f"The autoclicker hotkey is now '{args.hotkey}'.")
    update_config("hotkey", args.hotkey)
    sys.exit(0)
elif args.view:
    with open("./config.json", "r") as f:
        config = json.load(f)
    print("Current config\n\n")
    print(f"Speed: {config["speed"]}")
    print(f"Hotkey: {config["hotkey"]}\n")
elif args.clicker:
    clicker = Clicker()
    print("Ready! Press your hotkey to start clicking!")
    
    # Keep the program alive.
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("bravo six, goin' dark.")
elif args.gui:
    try:
        with open("./config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("failed to load config.")
        print("ensure that it is being created.")
        sys.exit(1)

    print("Running in GUI mode. Console will continue to be used as debug menu.")
    
    # We don't need the console to show up when running in GUI mode.
    if sys.platform.startswith('win'):
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
            ctypes.windll.kernel32.CloseHandle(hwnd)

    window = tk.Tk()
    window.title("Zero's Autoclicker GUI")
    window.geometry("350x200")
    window.minsize(200, 200)

    # Window icon needs to be set manually.
    if DEV:
        icon = Image.open("../assets/icon.png")
    else:
        icon = Image.open("assets/icon.png")
    photo = ImageTk.PhotoImage(icon)
    window.wm_iconphoto(False, photo)

    labeltext = tk.StringVar(window, f"Waiting for user input... ({config["hotkey"]})")
    label = tk.Label(window, textvariable=labeltext, height=4).pack(side=tk.TOP)

    clicker = Clicker(labeltext)

    startbutton = tk.Button(window, text="Start", height=2, command=lambda: clicker.trigger(True)).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    endbutton = tk.Button(window, text="Stop", height=2, command=lambda: clicker.trigger(False)).pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    window.mainloop()
