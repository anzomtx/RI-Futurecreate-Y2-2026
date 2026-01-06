import time
from machine import Pin, I2C
from VL53L0X import VL53L0X

# Initialize I2C bus
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Create a VL53L0X object
tof = VL53L0X(i2c)

# Start continuous ranging
tof.start()

try:
    while True:
        # Read the distance in millimeters
        distance = tof.read()
        print(f"Distance: {distance} mm")
        time.sleep_ms(100)  # Short delay between readings
        
except KeyboardInterrupt:
    # Stop the sensor and clean up on exit
    tof.stop()
    print("Stopped.")


