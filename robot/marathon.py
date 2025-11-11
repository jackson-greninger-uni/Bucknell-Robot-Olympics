from ultrasound import Ultrasound
from machine import Pin
import time
import neopixel

from line_follow import LineFollowerRobot
import neopix_buzzer
import uasyncio as asyncio

async def line_task(robot):
    robot.follow_line()
    await asyncio.sleep(0.001)

async def distance_task():
    # create the buzzer
    buzzer = machine.PWM(machine.Pin(22))
    # create the variable to handle distance sensing
    ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
    pixels = neopixel.NeoPixel(machine.Pin(18), 2)
    duty_cycle = 0.5

    while True:
        neopix_buzzer.normal_mode(ultrasound, pixels, buzzer, duty_cycle)
        await asyncio.sleep(0.001)

async def main():
    robot = LineFollowerRobot(velocity=30, kp=0.35, kd=0.01)
    await asyncio.gather(line_task(robot), distance_task())

asyncio.run(main())