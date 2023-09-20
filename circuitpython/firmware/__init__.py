import time

import usb_hid
from firmware import config

from .gamepad import Gamepad
from .pin_finder import PinFinder


def init():
    usb_hid.enable((Gamepad.DEVICE,))


def start(state: dict):
    mapping = config.get_mapping()
    verbose = config.get_bool("verbose")
    gamepad = Gamepad(usb_hid.devices, mapping, verbose=verbose)
    if config.get_bool("auto"):
        auto(gamepad)
        return
    listeners = [gamepad]
    if config.get_bool("conf"):
        listeners.append(PinFinder())
    state["listeners"] = listeners


def update(dt, listeners):
    for listener in listeners:
        listener.update()


def auto(gamepad: Gamepad):
    while True:
        for button in gamepad.mapping_full:
            print("Pressing", button)
            gamepad.press_buttons(button)
            time.sleep(1)
            gamepad.release_all_buttons()
        print("Pressing all buttons")
        gamepad.press_buttons(*gamepad.mapping_full.keys())
        time.sleep(1)
        gamepad.release_all_buttons()
