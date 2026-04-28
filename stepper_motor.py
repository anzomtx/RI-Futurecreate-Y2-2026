from machine import Pin
import stepper
import time

# Initialize GPIO pins
In1 = Pin(32, Pin.OUT)
In2 = Pin(33, Pin.OUT)
In3 = Pin(25, Pin.OUT)
In4 = Pin(26, Pin.OUT)

# Create a stepper motor object
s1 = stepper.create(In1, In2, In3, In4, delay=2)


def move_for_seconds(direction, seconds):
    """
    Move continuously for a set amount of time.

    direction:
        1  = clockwise
        -1 = counter-clockwise

    seconds:
        how long to keep moving
    """
    start = time.ticks_ms()
    duration = seconds * 1000

    while time.ticks_diff(time.ticks_ms(), start) < duration:
        s1.step(direction)


def move_steps_over_time(steps, seconds):
    """
    Move a specific number of steps over a specific duration.

    steps:
        positive = clockwise
        negative = counter-clockwise

    seconds:
        how long the movement should take
    """
    total_steps = abs(steps)

    if total_steps == 0:
        return

    direction = 1 if steps > 0 else -1
    step_interval_ms = int((seconds * 1000) / total_steps)

    for _ in range(total_steps):
        s1.step(direction)
        time.sleep_ms(step_interval_ms)
        

def move_angle_over_time(angle, seconds, steps_per_revolution=4096):
    """
    Move a certain angle over a certain duration.

    angle:
        positive = clockwise
        negative = counter-clockwise

    seconds:
        how long the movement should take

    steps_per_revolution:
        number of steps for 360 degrees
    """
    steps = int((angle / 360) * steps_per_revolution)
    move_steps_over_time(steps, seconds)


while True:
    print('Move clockwise continuously for 5 seconds')
    move_for_seconds(1, 5)

    print('Move counter-clockwise continuously for 5 seconds')
    move_for_seconds(-1, 5)

    print('180 degrees clockwise over 5 seconds')
    move_angle_over_time(180, 5)    # 
    
    print('90 degrees counter-clockwise over 5 seconds')
    move_angle_over_time(-90, 5)   # 

    
    
    
    
    
