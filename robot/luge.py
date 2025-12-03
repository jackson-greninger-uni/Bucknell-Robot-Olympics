from util_line_follow import LineFollowerRobot
from util_drive import Robot
from util_ultrasound import Ultrasound
import machine
from machine import Pin
import neopixel
import time

buzzer = machine.PWM(machine.Pin(22))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
robot = LineFollowerRobot(velocity=25, kp=0.45, kd=0.003)

time.sleep(1.0)
# Wait until clear
while True:
    distance = ultrasound.measure()
    if distance >= 10:
        break
    time.sleep_ms(10)

# Follow line and should stop when sees a wall 
while True:
    robot.follow_line("stop", 10)
    time.sleep(0.1)