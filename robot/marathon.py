from ultrasound import Ultrasound
from machine import Pin
import time
import neopixel

from line_follow import LineFollowerRobot
import neopix_buzzer

if __name__ == "__main__":
    # create the buzzer
    buzzer = machine.PWM(machine.Pin(22))
    
    # create the variable to handle distance sensing
    ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))

    pixels = neopixel.NeoPixel(machine.Pin(18), 2)

    while True:
        neopix_buzzer.normal_mode()