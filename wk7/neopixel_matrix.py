# 1. import statements
import machine, neopixel, time, random


# 2. functions and variables 
# Initialize the NeoPixel matrix
# GPIO 19 controls the data line, and there are 64 LEDs.
n = 64
np = neopixel.NeoPixel(machine.Pin(19), n)

def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()
    
def cycle_effect():
    print(n)
    
    for i in range(4 * n):
        clear()

        # Turn the current LED on
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

def sparkle(delay=0.1):
    while True:
        pixel = random.randint(0, n - 1)
        color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
        np[pixel] = color
        np.write()
        time.sleep(delay)
        np[pixel] = (0, 0, 0) # Turn off

def color_wipe(color, delay=0.05):
    for i in range(n):
        np[i] = color
        np.write()
        time.sleep(delay)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait):
    while True:
        for j in range(255):
            for i in range(n):
                pixel_index = (i * 256 // n) + j
                np[i] = wheel(pixel_index & 255)
            np.write()
            time.sleep(wait)
            
def scanner(color, delay=0.1):
    while True:
        for col in range(8):
            clear()
            for row in range(8):
                # Calculate index for each row in the current column
                np[row * 8 + col] = color
            np.write()
            time.sleep(delay)

clear()


# 3. main loop
while True:
    # enable/disable each effect by commenting
    cycle_effect()

    #sparkle()

    #color_wipe((255, 0, 0))  # Red wipe
    #color_wipe((0, 0, 0))

    #rainbow_cycle(0.0)

    #scanner((0, 0, 255), delay=0.1)



