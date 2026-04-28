from machine import Pin, PWM
from time import sleep

# Initialize PWM on your chosen pins
motor_a = PWM(Pin(32), freq=500)
motor_b = PWM(Pin(33), freq=500)

def set_speed(speed):
    # Ensure speed stays within -1023 to 1023
    speed = max(min(speed, 1023), -1023)
    
    if speed > 0:
        motor_a.duty(speed)
        motor_b.duty(0)
    elif speed < 0:
        motor_a.duty(0)
        motor_b.duty(abs(speed))
    else:
        motor_a.duty(0)
        motor_b.duty(0)

print("Starting motor loop. Press Ctrl+C to stop.")

try:
    while True:
        # Ramp up Forward
        print("Ramping Forward...")
        for s in range(400, 1024, 50): # Start at 400 (TT motors usually need a minimum kick)
            set_speed(s)
            sleep(0.1)
        
        sleep(1) # Full speed for 1 second
        
        # Ramp down to Stop
        for s in range(1023, -1, -50):
            set_speed(s)
            sleep(0.05)
            
        sleep(0.5)
        
        # Ramp up Backward
        print("Ramping Backward...")
        for s in range(-400, -1024, -50):
            set_speed(s)
            sleep(0.1)
            
        sleep(1) # Full speed backward
        
        # Ramp down to Stop
        for s in range(-1023, 1, 50):
            set_speed(s)
            sleep(0.05)
            
        print("Cycle complete. Restarting...")
        sleep(1)

except KeyboardInterrupt:
    print("Stopping motor...")
    set_speed(0)
    motor_a.deinit()
    motor_b.deinit()
