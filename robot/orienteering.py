from util_line_follow import LineFollowerRobot
from util_ultrasound import Ultrasound
from util_neopix_buzzer import play_melody
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
            time.sleep_ms(10)
        line_robot.indicator = True
        line_robot.stop()
        play_melody("victory_short", pixels, buzzer)
        time.sleep(1)  
        pixels.fill((255,255,0))
        pixels.write()

        line_robot.robot.drive(0, math.radians(160))
        time.sleep(1.0)
        line_robot.stop()

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 3000:
            line_robot.follow_line("stop", 1)
            time.sleep_ms(10)
        line_robot.go_straight(10)
        time.sleep(0.65)
        line_robot.stop()
        set_station(2)

    elif get_station() == Stations.TWO:
        line_robot.robot.drive(0, math.radians(180))
        time.sleep(0.5)
        line_robot.stop()
        
        # makes it to the target station
        start = time.ticks_ms()
        while line_robot.indicator:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)
        line_robot.indicator = True
        line_robot.stop()
        play_melody("victory_short", pixels, buzzer)
        pixels.fill((0,0,255))
        pixels.write()
        time.sleep(1)

        # turn around
        line_robot.robot.drive(0, math.radians(120))
        time.sleep(1.0)
        line_robot.stop()

        # return home
        line_robot.go_straight(10)
        time.sleep(1.0)
        line_robot.robot.drive(0, -math.radians(30))
        time.sleep(0.5)
        line_robot.go_straight(10)
        time.sleep(0.25)
        line_robot.robot.drive(0, -math.radians(40))
        time.sleep(0.5)
        line_robot.go_straight(10)
        time.sleep(0.5)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 1500:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)

        line_robot.go_straight(10)
        time.sleep(0.7)
        line_robot.stop()
        
        set_station(3)

    elif get_station() == Stations.THREE:
        # initial right turn to orient toward station 3
        line_robot.robot.drive(0, math.radians(155))
        time.sleep(0.5)

        line_robot.go_straight(10)
        time.sleep(0.25)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 2000:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)

        # manual right turn to navigate curve
        line_robot.robot.drive(0, math.radians(50))
        time.sleep(0.5)
        line_robot.go_straight(10)
        time.sleep(0.25)

        # travel to station
        while line_robot.indicator:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)
        line_robot.indicator = True
        play_melody("victory_short", pixels, buzzer)
        pixels.fill((255,0,0))
        pixels.write()
        time.sleep(1)
        line_robot.stop()

        # turn around
        line_robot.robot.drive(0, math.radians(150))
        time.sleep(1.0)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 2500:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)

        line_robot.go_straight(10)
        time.sleep(1.5)

        line_robot.stop()

        set_station(4)

    elif get_station() == Stations.FOUR:
        # turn around to hit the same way it just came
        line_robot.robot.drive(0, math.radians(140))
        time.sleep(1.0)
        line_robot.stop()

        # get it on track
        line_robot.go_straight(10)
        time.sleep(0.5)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 1900:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)

        # manual left turn to navigate curve
        line_robot.robot.drive(0, -math.radians(50))
        time.sleep(0.5)
        line_robot.go_straight(10)
        time.sleep(0.25)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 5000:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)
        
        # turn around to hit the same way it just came
        line_robot.robot.drive(0, math.radians(80))
        time.sleep(1.0)

        # nudge onto the gray track
        line_robot.go_straight(10)
        time.sleep(0.5)

        # travel to station 4
        while line_robot.indicator:
            line_robot.follow_line("stop", 2)
            time.sleep_ms(10)
        line_robot.indicator = True
        play_melody("victory_short", pixels, buzzer)
        pixels.fill((0,255,0))
        pixels.write()
        time.sleep(1)
        line_robot.stop()
        break
        