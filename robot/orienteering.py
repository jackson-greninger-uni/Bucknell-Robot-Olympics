from util_line_follow import LineFollowerRobot
from util_ultrasound import Ultrasound
from machine import Pin
import neopixel
import time
import math

class Stations:
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

current_station = Stations.ONE

def set_station(value):
    global current_station
    current_station = value

def get_station():
    return current_station

# hardware for distance sensing
buzzer = machine.PWM(machine.Pin(22))
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
duty_cycle = 0.5  # percentage

line_robot = LineFollowerRobot(velocity=10, kp=0.35, kd=0.025, ultrasound=ultrasound, buzzer=buzzer, pixels=pixels)

while True:
    if get_station() == Stations.ONE:
        while line_robot.indicator:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(1)
        line_robot.stop()
        time.sleep(1)  
        pixels.fill((255,255,0))
        pixels.write()

        line_robot.robot.drive(0, math.radians(160))
        time.sleep(1.0)
        line_robot.stop()

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 3500:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)

        line_robot.stop()
        set_station(2)

    elif get_station() == Stations.TWO:

        line_robot.robot.drive(0, math.radians(180))
        time.sleep(0.5)
        line_robot.stop()
        break