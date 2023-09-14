PLAYSIDES = ("P1", "P2")
BUTTONS = ("SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7")

def get_mapping():
    result = {}
    for side in PLAYSIDES:
        for button in BUTTONS:
            key = f"{side}_{button}"
            pin = os.getenv(key)
            if not pin:
                pin = None
            result[key] = pin
    return result
