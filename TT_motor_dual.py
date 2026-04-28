from machine import Pin, PWM
from time import sleep

class Motor:
    def __init__(self, pin1, pin2, freq=500):
        self.p1 = PWM(Pin(pin1), freq=freq)
        self.p2 = PWM(Pin(pin2), freq=freq)
        self.current_speed = 0
        
    def move(self, speed):
        # Constraints speed between -1023 and 1023
        speed = max(min(speed, 1023), -1023)
        self.current_speed = speed
        
        if speed > 0:
            self.p1.duty(speed)
            self.p2.duty(0)
        elif speed < 0:
            self.p1.duty(0)
            self.p2.duty(abs(speed))
        else:
            self.p1.duty(0)
            self.p2.duty(0)

# Initialize motors
left_motor = Motor(25, 26)
right_motor = Motor(32, 33)

def ramp_drive(target_left, target_right, step=50, delay=0.05):
    """Gradually changes motor speeds to the target values simultaneously"""
    while (left_motor.current_speed != target_left or 
           right_motor.current_speed != target_right):
        
        # Calculate next step for Left Motor
        if left_motor.current_speed < target_left:
            new_left = min(left_motor.current_speed + step, target_left)
        else:
            new_left = max(left_motor.current_speed - step, target_left)
            
        # Calculate next step for Right Motor
        if right_motor.current_speed < target_right:
            new_right = min(right_motor.current_speed + step, target_right)
        else:
            new_right = max(right_motor.current_speed - step, target_right)
            
        left_motor.move(new_left)
        right_motor.move(new_right)
        sleep(delay)

# --- Main Loop ---
try:
    while True:
        print("Ramping up: Forward")
        ramp_drive(1023, 1023)
        sleep(1)
        
        print("Ramping down: Stop")
        ramp_drive(0, 0)
        sleep(0.5)
        
        print("Ramping up: Turning")
        ramp_drive(800, -800) # Pivot turn
        sleep(1)
        
        print("Ramping down: Stop")
        ramp_drive(0, 0)
        sleep(1)

except KeyboardInterrupt:
    print("Emergency Stop")
    left_motor.move(0)
    right_motor.move(0)
