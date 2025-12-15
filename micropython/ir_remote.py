from machine import Pin, time_pulse_us
import time

# Configure the IR receiver pin
ir_pin = Pin(14, Pin.IN)

# Key function: reads one pulse length
def read_pulse(trigger_level):
    # Waits for the pin to be at 'trigger_level', then times how long it stays
    try:
        # timeout of 26ms is longer than the longest NEC pulse
        width = time_pulse_us(ir_pin, trigger_level, 26000)
        if width < 0:
            return None
    except Exception:
        return None
    return width

print("Ready. Point your remote and press a button!")

while True:
    # Wait for the start of a signal (a long LOW pulse)
    while ir_pin.value() == 1:
        pass
    # Measure the first START pulse (should be ~9000 us for NEC)
    start_pulse = read_pulse(0)
    
    if start_pulse and 8000 < start_pulse < 10000:  # Valid NEC start pulse
        data_pulses = []
        # Now read the next 32 pulses (for 32-bit NEC data)
        for _ in range(32):
            high = read_pulse(1)  # High pulse
            low = read_pulse(0)   # Low pulse
            if high is None or low is None:
                break
            # A short high+long low (total ~2250us) is a '0' bit
            # A long high+short low (total ~1125us) is a '1' bit
            if high + low > 2000:
                data_pulses.append(1)
            else:
                data_pulses.append(0)
        
        if len(data_pulses) == 32:
            # Convert pulse list to a number
            received_code = 0
            for pulse in data_pulses:
                received_code = (received_code << 1) | pulse
            print("Raw Code:", hex(received_code))
    time.sleep(0.1)






    