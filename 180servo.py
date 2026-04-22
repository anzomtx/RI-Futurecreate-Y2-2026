# 1. import statements
from machine import Pin, PWM
import time

# 2. functions and variables 
# Define the GPIO pin for the servo signal
servo_pin = Pin(23)

# Create a PWM object
# Servos typically require a 50Hz frequency
pwm = PWM(servo_pin, freq=50)

# Function to set the servo angle
def set_servo_angle(angle):
    # Map the angle (0-180) to the appropriate PWM duty cycle
    # These values are typical for SG90 servos, adjust if needed
    # 0 degrees: duty ~20 (approx 1ms pulse)
    # 90 degrees: duty ~70 (approx 1.5ms pulse)
    # 180 degrees: duty ~120 (approx 2ms pulse)
    
    # Calculate duty based on angle (linear mapping)
    duty = int(20 + (angle / 180) * 100)
    pwm.duty(duty)

# 3. main loop
try:
    while True:
        set_servo_angle(0)   # Move to 0 degrees
        time.sleep(1)
        set_servo_angle(90)  # Move to 90 degrees
        time.sleep(1)
        set_servo_angle(180) # Move to 180 degrees
        time.sleep(1)

except KeyboardInterrupt:
    pwm.deinit() # De-initialize PWM on exit

