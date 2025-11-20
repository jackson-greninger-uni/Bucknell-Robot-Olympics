from util_line_follow import LineFollowerRobot
from util_drive import Robot
from util_ultrasound import Ultrasound
from machine import Pin
import neopixel
import time

buzzer = machine.PWM(machine.Pin(22))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
robot = LineFollowerRobot(velocity=10, kp=0.35, kd=0.025, ultrasound=ultrasound, buzzer=buzzer, pixels=pixels)


while ultrasound.measure() > 10:
    robot.follow_line("stop")
    time.sleep(0.1)

