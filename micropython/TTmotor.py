from machine import Pin, PWM
import time

# Define pins connected to the L9110S
MOTOR_A1A = 12  # Speed control pin (PWM)
MOTOR_A1B = 14  # Direction control pin

# Initialize pins
speed_pwm = PWM(Pin(MOTOR_A1A, Pin.OUT))
dir_pin = Pin(MOTOR_A1B, Pin.OUT)

# Set PWM frequency (common for motors: 100-1000 Hz)
speed_pwm.freq(500)

MIN_SPEED = 450

def motor_control(speed, direction):
    """
    Controls a single L9110S motor channel.
    Args:
        speed (int): 0 (stop) to 1023 (full speed).
        direction (int): 0 for one way, 1 for the opposite way.
    """
    # Implement minimum speed for movement, but allow zero for stopping
    if speed > 0 and speed < MIN_SPEED:
        speed = MIN_SPEED

    # Set direction
    dir_pin.value(direction)
    
    # Apply speed
    if direction == 0:
        speed_pwm.duty(speed)
    else:
        speed_pwm.duty(1023 - speed)
        
        
# Example sequence
try:
    print("Motor forward at 70% speed")
    motor_control(100, 0)  # Speed ~700, Direction 0
    time.sleep(3)
    
    print("Motor stop")
    motor_control(0, 0)    # Speed 0 stops the motor
    time.sleep(1)
    
    print("Motor backward at 40% speed")
    motor_control(10, 1)  # Speed ~400, Direction 1
    time.sleep(3)
    
    print("Motor stop")
    motor_control(0, 0)
    
except KeyboardInterrupt:
    motor_control(0, 0)  # Ensure motor stops on interrupt
    print("Program stopped.")


    