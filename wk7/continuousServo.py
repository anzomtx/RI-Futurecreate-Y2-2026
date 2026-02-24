# 1. import statements
import machine
import time


# 2. functions and variables 
# Initialize PWM on Pin 25 with 50Hz frequency
servo_pwm = machine.PWM(machine.Pin(23))
servo_pwm.freq(50)

# Function to map speed to duty cycle
def set_continuous_speed(speed):
    # Constrain speed to a range of -100 to 100
    speed = max(-100, min(100, speed))
    
    # Map speed to duty cycle values.
    duty = int(77 + (speed / 100) * (115 - 77)) # For clockwise/counter-clockwise
    servo_pwm.duty(duty)


# 3. main loop
try:
    while True:
        # Rotate clockwise at half speed
        set_continuous_speed(50)
        time.sleep(2)
        
        # Stop
        set_continuous_speed(0)
        time.sleep(1)
        
        # Rotate counter-clockwise at half speed
        set_continuous_speed(-50)
        time.sleep(2)
        
        # Stop
        set_continuous_speed(0)
        time.sleep(1)
        
except KeyboardInterrupt:
    # Stop the servo and cleanup when interrupting the script
    servo_pwm.duty(0)
    servo_pwm.deinit()
    print("Stopped and cleaned up.")
