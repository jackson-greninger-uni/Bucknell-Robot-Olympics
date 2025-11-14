from line_follow import LineFollowerRobot
from drive import Robot
import time
from machine import Pin

# From start to center is 2.25 m
# Line len is 1.5 m
LINE_LEN = 1.5
# white distance is 0.75 m, 
SPRINT_LEN = 0.75
# robot should follow the line then go forward 0.75 m and stop


# Initialize the line-following robot with desired parameters
line_robot = LineFollowerRobot(velocity=40, kp=0.35, kd=0.05)



#robot on the line
while line_robot.last_offset != 0.00:
    line_robot.follow_line()
    print(f"Offset: {line_robot.last_offset:.2f}")
    time.sleep(0.01)


line_robot.robot.stop()


    
    