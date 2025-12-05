# import neopix_buzzer
import machine import Pin
import time
import math
from util_ultrasound import Ultrasound
from util_line_sensor import LineReader
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

        # reflectance sampling
        self.line_reader = LineReader(
            pins=[Pin(5 - x) for x in range(5)],
            positions=[-10, -5, -2, 4, 8]
        )

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
            v_left = angular_v * (self.wheel_base / 2)
            v_right = -angular_v * (self.wheel_base / 2)

        # TURN WHILE MOVING
        else:
            v_left = linear_v + (angular_v * self.wheel_base / 2)
            v_right = linear_v - (angular_v * self.wheel_base / 2)

        return v_left, v_right
    
    def navigate_obstacle(self, threshold=15):
        # turn 90 right
        self.drive(0, math.radians(130))
        time.sleep(0.5)

        # straight
        self.drive(10, math.radians(0))
        time.sleep(1.0)

        # turn 90 left
        self.drive(0, -math.radians(130))
        time.sleep(0.5)

        # straight (length of the obstacle)
        self.drive(10, math.radians(0))
        time.sleep(1.0)

        # turn 90 left
        self.drive(0, -math.radians(130))
        time.sleep(0.5)

        # straight until we hit the line
        while True:
            # straight
            self.drive(10, math.radians(0))
            print(self.line_reader.offset)
            time.sleep_ms(10)

        # turn 90 right
        self.drive(0, math.radians(120))
        time.sleep(0.5)


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
    
    robot.navigate_obstacle()