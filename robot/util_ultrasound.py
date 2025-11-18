# This code reads the distance using HC-SR04P (3-5V) ultrasonic sensor
# via default (trig-echo) mode and print out on serial.
# ---
# Connection: VCC=3.3V, TRIG = GP5, ECHO = GP4, GND = GND
# ---

from machine import Pin, PWM
import time

class Ultrasound():
    def __init__(self, trigger, echo):
        self.t = trigger
        self.e = echo
    
    def measure(self):
	    # create trigger pulse
        self.t.low()
        time.sleep_us(2)
        self.t.high()
        time.sleep_us(15)
        self.t.low()

	    # Wait for echo to go high
        timeout = time.ticks_us()
        while self.e.value() == 0:
            if time.ticks_diff(time.ticks_us(), timeout) > 1000000:
                print("ERROR: no echo start")
                return None
        start = time.ticks_us()

	    # measure echo width
        while self.e.value() == 1:
            if time.ticks_diff(time.ticks_us(), start) > 1000000:
                print("ERROR: echo stuck high")
                return None
        
        end = time.ticks_us()
        # compute width
        duration = time.ticks_diff(end, start)
        duration = duration / 1000
        
        # return distance
        return (17.4 * duration) + (-0.633)

if __name__ == "__main__":
    speaker = machine.PWM(machine.Pin(15))
    
    ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))

    duty_cycle = 1.0  # percentage
    
    while True:
        distance = ultrasound.measure()
        print(f"Distance = {distance:.2f} cm" if distance is not None else "Out of range")
        if distance is not None:
            tone = int(200 + (2000 / (distance + 1)))
            tone = min(max(tone, 100), 4000)  # clamp

            speaker.freq(tone)
            speaker.duty_u16(int(tone * duty_cycle))

            #print(f"Distance = {ultrasound.measure():.2f} cm")

            time.sleep(0.1)
        time.sleep(0.1)
