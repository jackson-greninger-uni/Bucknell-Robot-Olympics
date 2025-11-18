from util_line_follow import LineFollowerRobot
from util_drive import Robot
import time
from machine import Pin
import neopixel

# ok so the goal is to create a queue of the previous 5 offsets

queue = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]     # init with all ones

line_robot = LineFollowerRobot(20, kp=0.35, kd=0.01)
pixels = neopixel.NeoPixel(machine.Pin(18), 2)

while abs(sum(queue)) > 0.001:
    line_robot.follow_line("stop")
    queue.pop(0)
    queue.append(line_robot.last_offset)
    time.sleep_ms(1)

print("go straight")
line_robot.go_straight(20)
time.sleep(2)
pixels.fill((0,0,255))
pixels.write()
time.sleep(0.7)
line_robot.stop()