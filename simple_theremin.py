import time
from machine import Pin, I2C, PWM
from VL53L0X import VL53L0X

# Initialize I2C and Sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
tof = VL53L0X(i2c)

# Set up a PWM output on Pin 18 for sound
speaker = PWM(Pin(18))
speaker.duty(12)  # Set volume (duty cycle)

tof.start()

try:
    while True:
        tof.read()
        freq = tof.read()  # Use distance as frequency
        if freq > 20 and freq < 2000:  # Constrain to audible range
            speaker.freq(freq)
        time.sleep_ms(50)
        
except KeyboardInterrupt:
    tof.stop()
    speaker.deinit()
    print("Stopped.")
