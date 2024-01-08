# Zero's Autoclicker

An open source autoclicker made in Python.

## Command Line Interface

Zero's Autoclicker can be used straight from the terminal if you prefer, with several useful commands.

## Set Up (GUI)

If you only plan on using ZA in its GUI mode (which is okay!), here's how you can set it up to do so.

### 1. Create the Shortcut

The first step is to create a shortcut to the executable so you don't have to navigate to ZA every time you want to start it.

To do this, right click and drag the executable onto your Desktop and click the "Create shortcut here" option.

### 2. Modify the Shortcut

By default, Windows will just run the autoclicker. You need to tell the autoclicker you want it to start in the GUI mode instead. You can do this by modifying the start command to include the GUI flag (`-g`, `--gui`).

First, right click your newly created shortcut and select "Properties". Then, in the "Target" field, add `-g` or `--gui` to the very end of the line. (outside the quotation marks!)

## Commands

### Speed Command

The speed command (`-s`, `--speed`) can be used to adjust the wait between each click. It is used like so:
```
# Change the speed to 0.2.
autoclicker -s 0.2

# Run as fast as possible (can cause programs to lock up!)
autoclicker -s 0
```

### Hotkey Command

The hotkey command (`-k`, `--hotkey`) allows you to customize what key ZA listens for. It is used like so:
```
autoclicker -k ctrl+3
```
If a key is not recognized, an error will be displayed, giving you a list of all accepted keys.

### View Command

The view command (`-v`, `--view`) can be used to view your current settings. It is used like so:
```
autoclicker -v
```

### Clicker Command

The clicker command (`-c`, `--clicker`) is the most important command. This will start up ZA so you can use it. When run, it will wait for you to press the set hotkey before clicking.
```
autoclicker -c
```

### GUI Command

The gui command (`-g`, `--gui`) will open ZA in GUI mode. While it will still listen for hotkey presses, it can also be manually toggled from the interactive GUI menu.