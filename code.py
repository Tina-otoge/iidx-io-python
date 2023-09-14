import time

from firmware import config

mapping = config.get_mapping()
print(mapping)

while True:
    time.sleep(1)
