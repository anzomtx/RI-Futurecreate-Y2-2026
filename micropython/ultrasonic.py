from hcsr04 import HCSR04
from time import sleep

# Initialize the sensor (adjust pins if you used different GPIOs)
sensor = HCSR04(trigger_pin=5, echo_pin=18)

while True:
    try:
        # Get the distance in centimeters
        distance_cm = sensor.distance_cm()
        print('Distance:', distance_cm, 'cm')
        sleep(.5)
    except OSError as e:
        # Handle errors, for example when the measurement times out
        print("Sensor error or out of range:", e)

        