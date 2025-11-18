from util_line_follow import LineFollowerRobot
import time

robot = LineFollowerRobot(velocity=20, kp=0.45, kd=0.01)
while True:
    robot.follow_line("stop")
    time.sleep_ms(1)