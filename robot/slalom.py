from line_follow import LineFollowerRobot
import time

robot = LineFollowerRobot(velocity=20, kp=0.35, kd=0.025)
while True:
    robot.follow_line()
    time.sleep_ms(1)