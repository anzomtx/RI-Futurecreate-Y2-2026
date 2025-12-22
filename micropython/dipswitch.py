from machine import Pin
import time

# Define the number of positions and the GPIO pins for each switch
POSITION_NUM = 5
SWITCH_PINS = [18, 5, 17, 16, 4]  # Update these based on your wiring

ON = 0
OFF = 1

switches = []
for pin_num in SWITCH_PINS:
    switches.append(Pin(pin_num, Pin.IN))

print("DIP Switch Reader Started...")

try:
    while True:
        # Read and print the state of each switch position
        for i in range(POSITION_NUM):
            state = switches[i].value()
            if state == ON :
                status = "ON"
            else:
                status = "OFF"
                
            print(f"Position {i+1}: {status}")
        
        print()  # Print an empty line for readability
        time.sleep(0.5)  # Wait half a second before reading again

except KeyboardInterrupt:
    print("Program stopped.")