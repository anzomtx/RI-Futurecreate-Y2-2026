from machine import ADC, Pin
import time

# Setup: Connect sensor A0 to ESP32 GPIO14
sensor_analog = ADC(Pin(14))

# Set measurement range to 0-3.3V
sensor_analog.atten(ADC.ATTN_11DB)  

while True:
    # Read the raw analog value (0-4095 on ESP32)
    analog_value = sensor_analog.read()

    # Convert the raw value to a voltage
    voltage = (analog_value / 4095) * 3.3

    print(f"Raw ADC: {analog_value:4d} | Voltage: {voltage:.2f}V")
    time.sleep(0.2)


