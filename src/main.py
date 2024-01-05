import pyautogui
import argparse
import threading
import keyboard
import json
import os, sys
from time import sleep

# Ensure we run from the location of the executable.
os.chdir(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", help="The speed of the autoclicker.")
parser.add_argument("-k", "--hotkey", help="The toggle hotkey.")
parser.add_argument("-v", "--view", action="store_true", help="View current config.")
parser.add_argument("-c", "--clicker", action="store_true", help="Start the autoclicker.")

args = parser.parse_args()

pyautogui.PAUSE = 0

class Clicker:
    def __init__(self) -> None:
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        self.running = False

        hotkey = threading.Thread(name="hotkey_loop", target=self.__hotkey_loop)
        hotkey.daemon = True
        hotkey.start()

    def __clicker_loop(self):
        while self.running:
            pyautogui.click()
            sleep(self.config["speed"])

    def __hotkey_loop(self):
        """ 
        Loop for checking pressed keys to see if it matches the user hotkeys.
        """
        # Only handle one instance of the key press at once.
        pressed = False
        
        while True:
            if keyboard.is_pressed(self.config["hotkey"]) and not pressed:
                pressed = True

            if pressed:
                while True:
                    if not keyboard.is_pressed(self.config["hotkey"]):
                        pressed = False
                        break
                    sleep(0.001)
                
                if self.running == True:
                    print("Stopped autoclicker.")
                    self.running = False
                else:
                    print("Started autoclicker.")
                    self.running = True

                    # Start the autoclicker.
                    clicker = threading.Thread(name="clicker_loop", target=self.__clicker_loop)
                    clicker.daemon = True
                    clicker.start()

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
