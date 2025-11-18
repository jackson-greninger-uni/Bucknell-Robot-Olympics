from util_line_follow import LineFollowerRobot
import time

robot = LineFollowerRobot(velocity=15, kp=0.6, kd=0.01)
while True:
    robot.follow_line("stop")
    time.sleep_ms(1)