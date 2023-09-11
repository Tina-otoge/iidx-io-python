import usb_hid

from hid_gamepad import Gamepad

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     Gamepad.DEVICE
    )
)
