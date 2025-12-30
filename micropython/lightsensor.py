
from machine import ADC, Pin
import utime  # For timing functions

AO_PIN = ADC(Pin(14))  

# Set the ADC width (resolution) to 12 bits
AO_PIN.width(ADC.WIDTH_12BIT)

# Set the attenuation to 11 dB, allowing input range up to ~3.3V
AO_PIN.atten(ADC.ATTN_11DB)

while True:
    light_value = AO_PIN.read()  # Read the analog value (0-4095)
    print(light_value)  # Print the analog value

    utime.sleep(1)  # Add a small delay to avoid spamming the output
