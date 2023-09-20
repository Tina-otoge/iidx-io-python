import time

import board
import microcontroller
from digitalio import DigitalInOut, Direction, Pull


class PinFinder:
    def __init__(self):
        pins = {}
        for name in dir(microcontroller.pin):
            pin = getattr(microcontroller.pin, name)
            if not isinstance(pin, microcontroller.Pin):
                continue
            if pin is board.LED:
                continue
            try:
                switch = DigitalInOut(pin)
            except ValueError as e:
                print(f"conf mode could not init pin {pin}. Error:")
                print(e)
                continue
            switch.direction = Direction.INPUT
            switch.pull = Pull.UP
            pins[name] = switch
        self.pins = pins
        self.last_state = {}

    def get_state(self):
        return {
            pin: not switch.value
            for pin, switch in self.pins.items()
        }

    def update(self):
        state = self.get_state()
        for pin, value in state.items():
            if value != self.last_state.get(pin):
                print(time.monotonic())
                print(pin, "is now", value)
        self.last_state = state
