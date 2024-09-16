import time

import microcontroller
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from hid_gamepad import Gamepad


class Gamepad(Gamepad):
    GAMEPAD_REPORT_DESCRIPTOR = bytes((
        0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
        0x09, 0x05,  # Usage (Game Pad)
        0xA1, 0x01,  # Collection (Application)
        0x85, 0x04,  #   Report ID (4)
        0x05, 0x09,  #   Usage Page (Button)
        0x19, 0x01,  #   Usage Minimum (Button 1)
        0x29, 0x10,  #   Usage Maximum (Button 16)
        0x15, 0x00,  #   Logical Minimum (0)
        0x25, 0x01,  #   Logical Maximum (1)
        0x75, 0x01,  #   Report Size (1)
        0x95, 0x10,  #   Report Count (16)
        0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
        0x15, 0x81,  #   Logical Minimum (-127)
        0x25, 0x7F,  #   Logical Maximum (127)
        0x09, 0x30,  #   Usage (X)
        0x09, 0x31,  #   Usage (Y)
        0x09, 0x32,  #   Usage (Z)
        0x09, 0x35,  #   Usage (Rz)
        0x75, 0x08,  #   Report Size (8)
        0x95, 0x04,  #   Report Count (4)
        0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,        # End Collection
    ))

    DEVICE = usb_hid.Device(
        report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
        usage_page=0x01,           # Generic Desktop Control
        usage=0x05,                # Gamepad
        report_ids=(4,),           # Descriptor uses report ID 4.
        in_report_lengths=(6,),    # This gamepad sends 6 bytes in its report.
        out_report_lengths=(0,),   # It does not receive any reports.
    )

    def __init__(self, devices, mapping: dict, verbose: bool):
        super().__init__(devices)
        self.mapping_full = mapping
        self.mapping : dict[int, DigitalInOut] = {}
        self.verbose = verbose
        for key, pin in self.mapping_full.items():
            if not pin:
                self.log(f"Found no binding for button {key}, ignoring...")
                continue
            pin = getattr(microcontroller.pin, pin)
            switch = DigitalInOut(pin)
            switch.direction = Direction.INPUT
            switch.pull = Pull.UP
            self.mapping[key] = switch
            if self.verbose:
                self.log(f"Bound button {key} to pin {pin}")
        self.last_state = {}

    def get_state(self):
        return {
            button: not switch.value
            for button, switch in self.mapping.items()
        }

    def update(self):
        pressed = []
        released = []
        state = self.get_state()
        for button, value in state.items():
            if value:
                pressed.append(button)
            else:
                released.append(button)
        self.press_buttons(*pressed)
        self.release_buttons(*released)

        # We do not waste time saving last state when not in verbose mode, as
        # doing so is only useful for debug purposes
        if self.verbose:
            for button, value in state.items():
                if value != self.last_state.get(button):
                    self.log("Button", button, "is now", value)
            self.last_state = state

    def log(self, *args, **kwargs):
        if not self.verbose:
            return
        print(time.monotonic())
        print(*args, **kwargs)
