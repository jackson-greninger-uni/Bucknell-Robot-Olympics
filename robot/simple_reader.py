from machine import Pin
import time

def reflectance_sample(pins, samples, delay_us):
    pulse_widths = [0, 0, 0, 0, 0, 0]

    # charge capacitance
    pins[1].init(Pin.OUT, value=1)
    pins[2].init(Pin.OUT, value=1)
    pins[3].init(Pin.OUT, value=1)
    pins[4].init(Pin.OUT, value=1)
    pins[5].init(Pin.OUT, value=1)
    pins[0].init(Pin.OUT, value=1)
    time.sleep_us(30)

    # change to input
    pins[1].init(Pin.IN, pull = None)
    pins[2].init(Pin.IN, pull = None)
    pins[3].init(Pin.IN, pull = None)
    pins[4].init(Pin.IN, pull = None)
    pins[5].init(Pin.IN, pull = None)
    pins[0].init(Pin.IN, pull = None)

    for i in range(samples):
        # wait one sample period
        time.sleep_us(delay_us)
        # count the number of 1's
        pulse_widths[1] += pins[1].value()
        pulse_widths[2] += pins[2].value()
        pulse_widths[3] += pins[3].value()
        pulse_widths[4] += pins[4].value()
        pulse_widths[5] += pins[5].value()
        pulse_widths[0] += pins[0].value()

    for i in range(len(pulse_widths)):
        pulse_widths[i] *= delay_us
        
    # the pulse width is the number of 1's 
    # detected times the delay
    return pulse_widths

if __name__=="__main__":    
    # list of input pins for light sensor
    pins = [Pin(5-x) for x in range(6)]
    positions = [-20, -12, -4, 4, 12, 20]

    while True:
        ##########
        # original sample run
        ##########
        d = reflectance_sample(pins, 
                samples = 40, delay_us = 15)
        
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
        position = 0
        for i in range(len(d)):
            position += d[i] * positions[i]

        time.sleep(0.5)