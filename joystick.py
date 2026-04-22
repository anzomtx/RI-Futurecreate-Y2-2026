# 1. import statements
from DIYables_MicroPython_Joystick import Joystick
from machine import Pin, ADC
import time

# 2. functions and variables 
VRX_PIN = 33 # connect to VRX pin of joystick
VRY_PIN = 32 # connect to VRY pin of joystick
SW_PIN = 25  # connect to SW pin of joystick

adc_vrx = ADC(Pin(VRX_PIN))
adc_vry = ADC(Pin(VRY_PIN))
# Set the ADC width (resolution) to 12 bits
adc_vrx.width(ADC.WIDTH_12BIT)
adc_vry.width(ADC.WIDTH_12BIT)
# Set the attenuation to 11 dB, allowing input range up to ~3.3V
adc_vrx.atten(ADC.ATTN_11DB)
adc_vry.atten(ADC.ATTN_11DB)

joystick = Joystick(pin_x=VRX_PIN, pin_y=VRY_PIN, pin_button=SW_PIN)

# Configure the debounce time if necessary (default is 50ms)
joystick.set_debounce_time(100)  # debounce time set to 100 milliseconds


# 3. main loop
while True:
    joystick.loop()  # Must be called frequently to process button debouncing

    # Read the analog values from the X and Y axes
    x_value = joystick.read_x()
    y_value = joystick.read_y()
    press_count = joystick.get_press_count()

    # Check if the button has been pressed or released
    if joystick.is_pressed():
        print("Button Pressed")
    if joystick.is_released():
        print("Button Released")

    # Print the joystick's X and Y coordinates, and pressed count
    print(f'Joystick Position - X: {x_value}, Y: {y_value}, pressed count: {press_count}')

    time.sleep(0.1)  # Delay to reduce the output frequency
