import time
from simple_reader import reflectance_sample
from drive import Robot
from machine import Pin

class LineReader:

    def __init__(self, pins, positions):
        self.positions = positions
        self.pins = pins
        self.offset = 0.0

    def update(self):
        self.offset = 0

        ##########
        # original sample run
        ##########
        d = reflectance_sample(self.pins, samples=40, delay_us=15)
        
        ##########
        # subtract the minimum value
        ##########
        min_pulse = min(d)
        for i in range(len(d)):
            d[i] -= min_pulse
        
        ##########
        # find the sum of the array
        ##########
        summation = sum(d)
        ##########
        # normalize it
        ##########
        for i in range(len(d)):
            if summation == 0:
                d[i] = 0
            else:
                d[i] /= summation
        ##########
        # calculate the position based on the positions array
        ##########
        self.offset = 0
        for i in range(len(d)):
            self.offset += d[i] * self.positions[i]

if __name__ == "__main__":
    while True:
        reader = LineReader(
            pins = [Pin(5-x) for x in range(5)],
            positions = [-10, -5, -2, 2, 5]
        )
        reader.update()