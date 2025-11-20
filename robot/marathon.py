from util_line_follow import LineFollowerRobot
from util_ultrasound import Ultrasound
from machine import Pin
import neopixel
import time

# hardware for distance sensing
buzzer = machine.PWM(machine.Pin(22))
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
duty_cycle = 0.5  # percentage

robot = LineFollowerRobot(velocity=10, kp=0.35, kd=0.01, ultrasound=ultrasound, buzzer=buzzer, pixels=pixels)

while robot.indicator:
    robot.follow_line("stop")
    time.sleep_ms(1)