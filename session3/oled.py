# 1. import statements
from machine import Pin, I2C
import sh1106
import time


# 2. functions and variables 
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = 0x3C  
counter = 0  # Initialize our counter variable

devices = i2c.scan()

if addr not in devices:
    print(f"Display not found at 0x{addr:02X}")
else:
    print(f"Display found! Starting counter...")
    display = sh1106.SH1106(128, 64, i2c, addr=addr)


# 3. main loop
while True:
    # Clear the previous frame
    display.fill(0)
    
    # Draw header
    display.text("RUNNING COUNTER", 0, 0, 1)
    display.hline(0, 10, 128, 1)
    
    # Display the current count
    # Note: text() requires a string, so we use f-string or str()
    display.text(f"Value: {counter}", 30, 30, 1)
    
    # Update the physical screen
    display.show()
    
    # Increment and wait
    counter += 1
    time.sleep(1)


