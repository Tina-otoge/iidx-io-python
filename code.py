import time

import board
import digitalio
import usb_hid

from hid_gamepad import Gamepad

TIMER = 2

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
gamepad = Gamepad(usb_hid.devices)


while True:
    led.value = True
    print("LED ON")
    gamepad.press_buttons(1)
    time.sleep(TIMER)
    led.value = False
    print("LED OFF")
    gamepad.release_buttons(1)
    time.sleep(TIMER)
