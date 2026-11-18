
from pyfirmata2 import Arduino
import time

PORT = '/dev/ttyACM0'  # Fedora Linux
LASER_PIN = 7

board = Arduino(PORT)
laser = board.get_pin('d:7:o')

try:
    while True:
        laser.write(1)  # ON
        time.sleep(1)

        laser.write(0)  # OFF
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    laser.write(0)
    board.exit()
