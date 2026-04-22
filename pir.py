from machine import Pin
from time import sleep

# Initialize components
pir = Pin(14, Pin.IN)   # Sensor on GPIO 14
motion_detected = False # Global flag for motion

# Interrupt Service Routine (ISR)
def handle_motion(pin):
    global motion_detected
    motion_detected = True

# Attach the interrupt to the sensor pin
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_motion)

# Main loop
while True:
    if motion_detected:
        print("Motion detected! Turning LED on.")
        sleep(2)       # Wait 2 seconds before checking again
        motion_detected = False # Reset the flag

