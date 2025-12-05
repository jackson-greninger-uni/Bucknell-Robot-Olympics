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
robot = LineFollowerRobot(velocity=100, kp=0.01, kd=0.1, ultrasound=ultrasound, buzzer=buzzer, pixels=pixels)

# Another idea, but don't know if the continue in loop will work
#while True:
#    distance = ultrasound.measure()
#    if distance < 10:
#        continue
#    else:
#        robot.follow_line("stop")
#        time.sleep(0.5)

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


