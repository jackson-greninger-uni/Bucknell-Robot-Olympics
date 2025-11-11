# import neopix_buzzer
import machine
import time
import math
from ultrasound import Ultrasound
# import neopixel

global buzzer, pixels, duty_cycle, ultrasound

class Robot:
    def __init__(self, bias=-0.03, freq=8000, wheel_base=13):
        # Motor bias (left/right compensation)
        self.left_bias = 1.0 - bias / 2
        self.right_bias = 1.0 + bias / 2

        # Motion parameters
        self.duty = 0
        self.wheel_base = wheel_base

        # PWM setup for motors
        self.M1A = machine.PWM(machine.Pin(8))
        self.M1B = machine.PWM(machine.Pin(9))
        self.M2A = machine.PWM(machine.Pin(10))
        self.M2B = machine.PWM(machine.Pin(11))
        for m in [self.M1A, self.M1B, self.M2A, self.M2B]:
            m.freq(freq)

    def velocity_to_duty(self, velocity):
        return 997 * abs(velocity) + 15362

    def set_motor(self, motor_a, motor_b, duty, direction, bias):
        duty_val = int(duty * bias)
        
        if duty_val > 65536:
            duty_val = 65536
        
        if direction >= 0:
            motor_a.duty_u16(duty_val)
            motor_b.duty_u16(0)
        else:
            motor_a.duty_u16(0)
            motor_b.duty_u16(duty_val)

    def compute_wheel_velocities(self, linear_v, angular_v):
        # MOVE STRAIGHT
        if angular_v == 0:
            return linear_v, linear_v

        # TURN IN PLACE
        elif linear_v == 0:
            if angular_v < 0:
                v_left = -angular_v * (self.wheel_base / 2)
                v_right = angular_v * (self.wheel_base / 2)
            else:
                v_left = angular_v * (self.wheel_base / 2)
                v_right = -angular_v * (self.wheel_base / 2)

        # TURN WHILE MOVING
        else:
            v_left = linear_v + (angular_v * self.wheel_base / 2)
            v_right = linear_v - (angular_v * self.wheel_base / 2)

        return v_left, v_right

    def drive(self, linear_v, angular_v):
        # STOP
        if linear_v == 0 and angular_v == 0:
            for motor in [self.M1A, self.M1B, self.M2A, self.M2B]:
                motor.duty_u16(0)
            return

        # Calculate wheel velocities
        v_left, v_right = self.compute_wheel_velocities(linear_v, angular_v)

        # Convert to PWM duty cycles
        duty_left = self.velocity_to_duty(v_left)
        duty_right = self.velocity_to_duty(v_right)

        # Apply to motors
        self.set_motor(self.M1A, self.M1B, duty_left, v_left, self.left_bias)
        self.set_motor(self.M2A, self.M2B, duty_right, v_right, self.right_bias)
        
        #print(f"v_left={v_left:.3f}, v_right={v_right:.3f}, "
        #      f"duty_left={duty_left:.0f}, duty_right={duty_right:.0f}")
    
    def stop(self):
        self.set_motor(self.M1A, self.M1B, 0, 0, self.left_bias)
        self.set_motor(self.M2A, self.M2B, 0, 0, self.right_bias)


if __name__ == "__main__":
    robot = Robot()
    
    # TEST 1 -- straight!
    # 20 cm/s, 0 rad/s 
    robot.drive (20, 0)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
    robot.drive (0, 0)
    time.sleep_ms(500)

    # TEST 2 -- reverse
    # -20 cm/s, 0 rad/s 
    robot.drive (-20, 0)
    time.sleep_ms(500)
    # stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
    robot.drive (0, 0)
    time.sleep_ms(500)

    # TEST 3 -- RIGHT
    robot.drive (20, math.radians(180))
    time.sleep_ms(500)
    # stop, robot should have turned about 90 degrees clockwise
    robot.drive (0, 0)
    time.sleep_ms(500)

    # TEST 4 -- LEFT
    robot.drive (20, -math.radians(180))
    time.sleep_ms(500)
    # stop, we should have turned about 180 degrees counter clockwise
    robot.drive (0, 0)
    time.sleep_ms(500)

    ## TEST 5 -- ROTATE in PLACE
    robot.drive (0, math.radians(360))
    time.sleep_ms(1000)
    # stop, robot should turn about 360 degrees clockwise
    robot.drive (0, 0)
    time.sleep_ms(500)