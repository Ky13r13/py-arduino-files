
from pyfirmata2 import Arduino, util
import time

board = Arduino("/dev/ttyACM0")

photo_res = board.get_pin("a:2:i")
touch = board.get_pin("d:3:i")
laser = board.get_pin("d:7:o")

previous = None
light_value = None
read_at = None

def on_light(value):
    global light_value
    light_value = value

def on_touch(value):
    global previous, read_at

    if value != previous:
        if value:
            laser.write(1)
            print("TOUCHED!", flush=True)
            read_at = time.monotonic() + 0.1
        else:
            laser.write(0)
            print("Released", flush=True)
            read_at = None

        previous = value

touch.register_callback(on_touch)
photo_res.register_callback(on_light)

touch.enable_reporting()
photo_res.enable_reporting()

iterator = util.Iterator(board)
iterator.start()

board.samplingOn(19)

print("Arduino connected!")

try:
    while True:
        if read_at is not None and time.monotonic() >= read_at:
            if light_value is not None:
                raw = int(light_value * 1023)
                voltage = light_value * 5.0

                print(f"Light: {light_value:.3f}")
                print(f"ADC: {raw}")
                print(f"Voltage: {voltage:.3f} V")

            read_at = None

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    laser.write(0)
    board.exit()
