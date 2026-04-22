from machine import Pin
import time

# Setup: Connect sensor D0 to ESP32 GPIO14
# The sensor's onboard potentiometer sets the trigger threshold.
sensor_digital = Pin(14, Pin.IN)

while True:
    # Value is 1 (HIGH/3.3V) when quiet, 0 (LOW/0V) when sound is detected.
    digital_state = sensor_digital.value()

    if digital_state == 1:
        print("Sound detected!")
    # Optional: Add action here, like turning on an LED
    time.sleep(0.05)  # Short delay for responsive checking

    