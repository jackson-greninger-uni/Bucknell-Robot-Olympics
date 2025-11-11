from line_sensor import LineReader
from drive import Robot
import time
from machine import Pin

# safe values:
# velocity = 10
#   when turning, 5
# kd = 0.01

class LineFollowerRobot:
    def __init__(self, velocity, kp=0.35, kd=0.05):
        self.reader = LineReader(
            pins=[Pin(5 - x) for x in range(5)],
            positions=[-10, -5, -2, 2, 5]
        )
        self.robot = Robot()

        # PD parameters
        self.kp = kp
        self.kd = kd

        # Motion state
        self.velocity = velocity
        self.last_offset = 0.0
        self.last_time_us = time.ticks_us() - 10000

        self.running = False

    def _compute_dt(self):
        current_time_us = time.ticks_us()
        dt_us = time.ticks_diff(current_time_us, self.last_time_us)
        self.last_time_us = current_time_us
        return dt_us / 1_000_000.0  # convert µs → seconds

    def _compute_control(self, error: float, dt: float):
        derivative = 0.0
        if dt > 0:
            derivative = (error - self.last_offset) / dt
            
        angular_velocity = (self.kp * error) + (self.kd * derivative)

        self.last_offset = error
        return angular_velocity
    
    def compute_velocity(self, error):
        x = abs(error)
        v_max = self.velocity
        v_min = 1       # You can tune this
        x_max = 10      # Max offset expected

        slope = (v_max - v_min) / x_max
        v = v_max - slope * x

        # Clamp so it doesn't go below v_min
        return max(v, v_min)

    def follow_line(self):
        self.running = True

        try:
            while self.running:
                # Update sensor readings
                self.reader.update()
                error = self.reader.offset

                # Compute timing and PD control
                dt = self._compute_dt()
                angular_velocity = self._compute_control(error, dt)

                current_velocity = self.compute_velocity(error)

                # Drive the robot
                self.robot.drive(current_velocity, angular_velocity)

                # Small delay to smooth loop timing
                time.sleep_ms(1)

        finally:
            self.stop()

    def stop(self):
        self.running = False
        self.robot.stop()