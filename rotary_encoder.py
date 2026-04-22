# 1. import statements
from machine import Pin
from rotary_irq_esp import RotaryIRQ

# 2. functions and variables 
# Initialize the rotary encoder with internal pull-ups enabled
rotary_encoder = RotaryIRQ(
    pin_num_clk=22,   # connect to CLK
    pin_num_dt=23,    # connect to DT
    pull_up=True      # Enable internal pull-up resistors
)

# Optional: set boundaries and wrapping
rotary_encoder.set(min_val=0, max_val=20, range_mode=RotaryIRQ.RANGE_WRAP)

last_value = rotary_encoder.value()


# 3. main loop
while True:
    current_value = rotary_encoder.value()
    
    if current_value != last_value:
        print("Counter value:", current_value)
        
        if current_value > last_value: 
        	direction = "increased" 
        else: 
        	direction = "decreased"

        print(f"Direction: {direction}")
        
        last_value = current_value

