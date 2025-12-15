from machine import Pin, I2C
import time

# Initialize I2C on the default bus (0) and pins
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Alternative I2C pins (if you are using different ones)
# i2c = I2C(0, scl=Pin(5), sda=Pin(4))

print("Scanning I2C bus...")
devices = i2c.scan()  # This returns a list of addresses

if len(devices) == 0:
    print("No I2C devices found!")
else:
    print(f"Found {len(devices)} device(s):")
    for device in devices:
        # Print address in decimal and hex format
        print(f"  - Decimal: {device} | Hex: 0x{device:02X}")