import time

import board
import digitalio
import microcontroller
import usb_hid
from digitalio import DigitalInOut, Direction, Pull

# from hid_gamepad import Gamepad
from microcontroller import Pin

BUTTONS_P1 = {
    "SW1": "GPIO10",
    "SW2": "GPIO13",
    "SW3": "GPIO11",
    "SW4": None,
    "SW5": "GPIO12",
    "SW6": "GPIO7",
    "SW7": "GPIO8",
}

BUTTONS_P2 = {
    "SW1": "GPIO13",
    "SW2": "GPIO10",
    "SW3": "GPIO9",
    "SW4": "GPIO9",
    "SW5": "GPIO7",
    "SW6": "GPIO12",
    "SW7": "GPIO11",
}

TIMER = 0.1

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
# gamepad = Gamepad(usb_hid.devices)

pins = {}
for name in dir(microcontroller.pin):
    pin = getattr(microcontroller.pin, name)
    if not isinstance(pin, Pin):
        continue
    if pin is board.LED:
        continue
    switch = DigitalInOut(pin)
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    pins[name] = switch

def get_state():
    return {
        name: switch.value
        for name, switch in pins.items()
    }

def dump_state(state):
    for name in state:
        print(f"{name}: {state[name]}")

last_state = get_state()
dump_state(last_state)

def is_same_state(state1, state2):
    for name in state1:
        if state1[name] != state2[name]:
            print(f"{name} changed from {state1[name]} to {state2[name]}")
            return False
    return True

last_change = time.time()

while True:
    now = time.time()
    # led.value = True
    # print("LED ON")
    # gamepad.press_buttons(1)
    # time.sleep(TIMER)
    # led.value = False
    # print("LED OFF")
    # gamepad.release_buttons(1)
    new_state = get_state()
    if not is_same_state(last_state, new_state):
        # dump_state(new_state)
        last_state = new_state
        last_change = now
        print(now)
        print("-" * 10)
    if now - last_change < 2:
        led.value = not led.value
    else:
        led.value = False
    time.sleep(TIMER)
