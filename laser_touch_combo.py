
from pyfirmata2 import Arduino, util
import time



board = Arduino("/dev/ttyACM0")
photo_res = board.get_pin("a:2:i")
touch = board.get_pin("d:3:i")
laser = board.get_pin('d:7:o')
previous = None

def on_touch(value):
    global previous

    if value != previous:
        if value:
            print("TOUCHED!", flush=True)
            laser.write(1) 
            light = photo_res.read()
            if light is not None:
                print(f"Light level: {light:.3f}")
                raw_value = int(light * 1023)
                voltage = light * 5.0
                print(voltage)
            
        else:
            print("Released", flush=True)
            laser.write(0)
        previous = value


touch.register_callback(on_touch)

# Enable digital input reporting
touch.enable_reporting()

iterator = util.Iterator(board)
iterator.start()
photo_res.enable_reporting()

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
    laser.write(0)
