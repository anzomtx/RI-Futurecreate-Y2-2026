from machine import Pin, PWM
from time import sleep

# Define Pins 12 and 14
motor_a = PWM(Pin(32), freq=500)
motor_b = PWM(Pin(33), freq=500)

def set_speed(speed):
    # L9110 logic: one HIGH (PWM), one LOW
    if speed > 0:
        motor_a.duty(abs(speed))
        motor_b.duty(0)
    elif speed < 0:
        motor_a.duty(0)
        motor_b.duty(abs(speed))
    else:
        motor_a.duty(0)
        motor_b.duty(0)

# Test sequence
# Speed is between -1023 to 1023

set_speed(1023) # Forward
sleep(2)
set_speed(-1023) # Backward
sleep(2)
set_speed(0)

