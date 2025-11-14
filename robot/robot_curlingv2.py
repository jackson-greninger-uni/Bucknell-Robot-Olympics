from line_follow import LineFollowerRobot
from drive import Robot
import time
from machine import Pin

# ok so the goal is to create a queue of the previous 5 offsets

queue = [1,1,1,1,1]     # init with all ones

line_robot = LineFollowerRobot(20, kp=0.35, kd=0.01)

while abs(sum(queue)) > 0.001:
    line_robot.follow_line()
    queue.pop(0)
    queue.append(line_robot.last_offset)
    time.sleep_ms(1)

line_robot.go_straight()
time.sleep(1)
line_robot.stop()