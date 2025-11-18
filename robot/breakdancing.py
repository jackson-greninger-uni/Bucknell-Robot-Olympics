from util_drive import Robot
import time
from util_neopix_buzzer import normal_mode
from machine import Pin
import math
from util_ultrasound import Ultrasound
import neopixel

#Breakdancing Qualifying

#Move in all directions
robot = Robot()
    
# TEST 1 -- straight!
# 20 cm/s, 0 rad/s 
robot.drive (20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
robot.drive (0, 0)
time.sleep_ms(500)
# TEST 2 -- reverse
# -20 cm/s, 0 rad/s 
robot.drive (-20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
robot.drive (0, 0)
time.sleep_ms(500)
# TEST 3 -- RIGHT
robot.drive (20, math.radians(180))
time.sleep_ms(500)
# stop, robot should have turned about 90 degrees clockwise
robot.drive (0, 0)
time.sleep_ms(500)
# TEST 4 -- LEFT
robot.drive (20, -math.radians(180))
time.sleep_ms(500)
# stop, we should have turned about 180 degrees counter clockwise
robot.drive (0, 0)
time.sleep_ms(500)


#Use neopixel and buzzer
buzzer = machine.PWM(machine.Pin(22))
# create the variable to handle distance sensing
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
duty_cycle = 0.5  # percentage
while True:
    normal_mode(ultrasound, pixels, buzzer, duty_cycle)




