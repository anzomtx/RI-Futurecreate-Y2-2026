# mpr121.py library
from machine import I2C

class MPR121:
    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address
        # Reset the sensor
        self._register8(0x80, 0x63)
        # Configuration settings
        self.set_thresholds(15, 7)
        self._register8(0x5E, 0x8C)  # Config 1
        self._register8(0x5F, 0x9A)  # Config 2
        # Enable all 12 electrodes
        self._register8(0x5E, 0x8C)
        self._register8(0x5F, 0x9A)

    def _register8(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    def _register16(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 2)
        return (data[1] << 8) | data[0]

    def set_thresholds(self, touch, release):
        for i in range(12):
            self._register8(0x41 + (2 * i), touch)
            self._register8(0x42 + (2 * i), release)

    def get_all_states(self):
        touched = self._register16(0x00)
        states = []
        for i in range(12):
            if touched & (1 << i):
                states.append(i)
        return states

    def is_touched(self, pin):
        touched = self._register16(0x00)
        return True if touched & (1 << pin) else False