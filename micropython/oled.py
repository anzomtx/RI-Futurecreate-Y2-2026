from machine import Pin, I2C
import sh1106
import time

# Initialize I2C with explicit frequency (helps stability)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Check if display is found
addr = 0x3C  # Try 0x3D if this doesn't work
devices = i2c.scan()

if addr not in devices:
    print(f"Display not found at 0x{addr:02X}")
    print("Found devices:", [hex(d) for d in devices])
else:
    print(f"Display found at 0x{addr:02X}")
    
    # Initialize display
    display = sh1106.SH1106(128, 64, i2c, addr=addr)
    
    # Display test pattern
    display.fill(0)
    display.text("OLED is Working!", 0, 0, 1)
    display.text("ESP32 + MicroPython", 0, 20, 1)
    display.rect(0, 40, 128, 20, 1)
    display.fill_rect(10, 45, 20, 10, 1)
    display.show()
    
    print("Display should show text and shapes")
    
    # Keep running
    while True:
        time.sleep(1)


