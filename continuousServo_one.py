import machine
import time

# Initialize PWM on Pin 23
servo_pwm = machine.PWM(machine.Pin(23))
servo_pwm.freq(50)

def set_continuous_speed(speed):
    # Constrain speed to -100 to 100
    speed = max(-100, min(100, speed))
    
    # 1,500,000ns is the center (Stop)
    # 500,000ns is the range in either direction
    pulse_ns = int(1500000 + (speed / 100) * 500000)
    
    # Set the pulse in nanoseconds
    servo_pwm.duty_ns(pulse_ns)

try:
    while True:
        print("Clockwise...")
        set_continuous_speed(50)
        time.sleep(2)
        
        print("Stopping...")
        set_continuous_speed(0)
        time.sleep(1)
        
        print("Counter-Clockwise...")
        set_continuous_speed(-50)
        time.sleep(2)
        
except KeyboardInterrupt:
    # Cleanup: turn off the pulse entirely
    servo_pwm.duty_ns(0)
    servo_pwm.deinit()
    print("PWM Deinitialized.")