import machine
import time

# Initialize Servo 1 on Pin 23
servo1 = machine.PWM(machine.Pin(23))
servo1.freq(50)

# Initialize Servo 2 on Pin 19
servo2 = machine.PWM(machine.Pin(19))
servo2.freq(50)

def set_speed(servo_obj, speed):
    speed = max(-100, min(100, speed))
    # 1.5ms (1500000ns) is stop
    pulse_ns = int(1500000 + (speed / 100) * 500000)
    servo_obj.duty_ns(pulse_ns)

try:
    while True:
        # Move both in opposite directions
        set_speed(servo1, 50)
        set_speed(servo2, -50)
        time.sleep(2)
        
        # Stop both
        set_speed(servo1, 0)
        set_speed(servo2, 0)
        time.sleep(1)
        
except KeyboardInterrupt:
    servo1.deinit()
    servo2.deinit()
    print("Cleanup complete.")