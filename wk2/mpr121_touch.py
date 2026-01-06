from mpr121 import MPR121
from machine import Pin, I2C
import utime

# Initialize I2C on bus 0 with SDA on GPIO 21 and SCL on GPIO 22
i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# Create an MPR121 object
mpr = MPR121(i2c)

print("Touch sensor ready. Start touching the electrodes!")

# Main loop to check all electrodes
while True:
    # Get a list of all currently touched electrodes
    touched_pins = mpr.get_all_states()
    if len(touched_pins) != 0:
        print(touched_pins)
    utime.sleep_ms(100)

    