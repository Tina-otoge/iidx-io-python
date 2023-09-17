import os

PLAYSIDES = ("P1", "P2")
BUTTONS = ("SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7")
BUTTONS_ALL = (
    f"{side}_{button}" for button in BUTTONS for side in PLAYSIDES
)


def get_mapping():
    result = {}
    index = 0
    for side in PLAYSIDES:
        for button in BUTTONS:
            index += 1
            key = f"{side}_{button}"
            pin = os.getenv(key)
            if not pin:
                pin = None
            result[index] = pin
    return result


def get_bool(key):
    key = f"ENABLE_{key.upper()}"
    value = os.getenv(key, False)
    if not value:
        return False
    return value.lower() in ("y", "yes", "true", "ok", "on")
