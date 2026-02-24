# 1. import statements
import machine
import time

# 2. functions and variables 
# Define the pin where the LED is connected
led = machine.Pin(5, machine.Pin.OUT)

print("Starting blink loop... Press Ctrl+C to stop.")

# 3. main loop
try:
    while True:
        led.value(1)    # Turn LED on
        time.sleep(0.5) # Wait for 500ms
        led.value(0)    # Turn LED off
        time.sleep(0.5) # Wait for 500ms
        
except KeyboardInterrupt:
    # Clean up: turn off LED when exiting
    led.value(0)
    print("Blink stopped.")