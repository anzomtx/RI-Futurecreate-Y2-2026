# Stepper.py
import time

class Stepper:
    FULL_ROTATION = 2048 # Approximate number of steps for a full revolution[citation:1][citation:2]
    HALF_STEP = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]

    def __init__(self, pin1, pin2, pin3, pin4, delay=2):
        self.pins = [pin1, pin2, pin3, pin4]
        self.delay = delay  # Delay between steps in milliseconds
        self._state = 0

    def step(self, steps):
        direction = 1 if steps >= 0 else -1
        steps = abs(steps)
        for _ in range(steps):
            state = self.HALF_STEP[self._state]
            for i, pin in enumerate(self.pins):
                pin.value(state[i])
            self._state = (self._state + direction) % len(self.HALF_STEP)
            time.sleep_ms(self.delay)

    def angle(self, degrees, direction=1):
        steps = int((degrees / 360) * self.FULL_ROTATION)
        self.step(steps * direction)

# Helper function to create a stepper instance
def create(pin1, pin2, pin3, pin4, delay=2):
    return Stepper(pin1, pin2, pin3, pin4, delay)