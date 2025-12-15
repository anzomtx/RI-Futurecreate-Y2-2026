from machine import Pin
import time

# Define the number of positions and the GPIO pins for each switch
POSITION_NUM = 5
SWITCH_PINS = [4, 16, 17, 5, 18]  # Update these based on your wiring

# Define what ON and OFF mean in terms of electrical state
# ON = LOW (because the pin is connected to GND)
# OFF = HIGH (because the pin is pulled up)
ON = 0
OFF = 1

# Set all switch pins as inputs with pull-up resistors enabled
switches = []
for pin_num in SWITCH_PINS:
    switches.append(Pin(pin_num, Pin.IN, Pin.PULL_UP))

print("DIP Switch Reader Started...")

try:
    while True:
        # Read and print the state of each switch position
        for i in range(POSITION_NUM):
            state = switches[i].value()
            status = "ON" if state == ON else "OFF"
            print(f"Position {i+1}: {status}")
        
        print()  # Print an empty line for readability
        time.sleep(0.5)  # Wait half a second before reading again

except KeyboardInterrupt:
    print("Program stopped.")