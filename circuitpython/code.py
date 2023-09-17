import os
import time

import firmware

state = {}
firmware.start(state)
test_mode = os.getenv("TEST_MODE", False)

last = time.monotonic()
while True:
    now = time.monotonic()
    dt = now - last
    if test_mode:
        firmware.test(dt, **state)
    firmware.update(dt, **state)
    last = now
