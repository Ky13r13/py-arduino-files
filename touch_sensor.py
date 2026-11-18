
import time
from pyfirmata2 import Arduino

board = Arduino("/dev/ttyACM0")

# Keyes touch sensor connected to D2
touch = board.get_pin("d:3:i")

previous = None

def on_touch(value):
    global previous

    if value != previous:
        if value:
            print("TOUCHED!", flush=True)
        else:
            print("Released", flush=True)

        previous = value

# Register callback
touch.register_callback(on_touch)

# Enable digital input reporting
touch.enable_reporting()

# IMPORTANT: Start the sampling thread
board.samplingOn(19)

print("Arduino connected!")
print("Sampling started. Touch the sensor.")

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    board.exit()
