from line_follow import LineFollowerRobot

robot = LineFollowerRobot(velocity=10, kp=0.35, kd=0.025)
robot.follow_line()