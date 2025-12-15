import machine
import neopixel
import time

# Initialize the NeoPixel matrix
# GPIO 19 controls the data line, and there are 64 LEDs.
np = neopixel.NeoPixel(machine.Pin(19), 64)

def cycle_effect(np):
    n = len(np)  # Get the number of LEDs (64)
    for i in range(4 * n):
        # Turn all LEDs off
        for j in range(n):
            np[j] = (0, 0, 0)
        # Turn the current LED on
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

# Run the cycle effect
cycle_effect(np)

