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
sprint_robot = Robot()


#robot on the line


sprint_robot.drive(40, 0)  # Move forward at 40 cm/s
time.sleep(SPRINT_LEN / 40)  # Time to cover the sprint distance
sprint_robot.stop()
    
    