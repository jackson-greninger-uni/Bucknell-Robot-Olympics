import time
from simple_reader import reflectance_sample

class LineReader:

    def __init__(self, pins, positions):
        self.positions = positions
        self.pins = pins
        self.offset = 0.0

    def update(self):
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
                d[i] == 0
            else:
                d[i] /= summation
        ##########
        # calculate the position based on the positions array
        ##########
        for i in range(len(d)):
            self.offset += d[i] * self.positions[i]

        time.sleep(0.5)