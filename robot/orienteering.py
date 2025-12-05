from util_line_follow import LineFollowerRobot
from util_ultrasound import Ultrasound
from machine import Pin
import neopixel
import time

from enum import Enum

class Stations(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

current_station = Stations.ONE

def get_station():
    return current_station

def set_station(station_value):
    global current_station
    # Allow user to pass int OR Stations enum
    if isinstance(station_value, int):
        current_station = Stations(station_value)
    elif isinstance(station_value, Stations):
        current_station = station_value

# hardware for distance sensing
buzzer = machine.PWM(machine.Pin(22))
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
duty_cycle = 0.5  # percentage

line_robot = LineFollowerRobot(velocity=10, kp=0.35, kd=0.025, ultrasound=ultrasound, buzzer=buzzer, pixels=pixels)
Stations.set_station(1)

if get_station() == Stations.ONE:
    while line_robot.indicator:
        line_robot.follow_line("stop", 2)
        time.sleep_ms(1)
        
    pixels.fill((0,255,0))
    pixels.write()