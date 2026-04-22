from machine import Pin
import Stepper

# Initialize GPIO pins
In1 = Pin(32, Pin.OUT)
In2 = Pin(33, Pin.OUT)
In3 = Pin(25, Pin.OUT)
In4 = Pin(26, Pin.OUT)

# Create a stepper motor object
s1 = Stepper.create(In1, In2, In3, In4, delay=2)

# Control the motor
#s1.step(100)       # Move 100 steps clockwise
#s1.step(-50)       # Move 50 steps counter-clockwise
s1.angle(180)       # Rotate 90 degrees clockwise
#s1.angle(180, -1) # Rotate 180 degrees counter-clockwise

