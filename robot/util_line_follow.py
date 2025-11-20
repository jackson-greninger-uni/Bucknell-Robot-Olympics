from util_line_sensor import LineReader
from util_drive import Robot
import time
from machine import Pin

# safe values:
# velocity = 10
#   when turning, 5
# kd = 0.01

class LineFollowerRobot:
    def __init__(self, velocity, kp=0.35, kd=0.05, ultrasound=None, buzzer=None, pixels=None):
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

        # hardware for obstacle detection
        self.ultrasound = ultrasound
        self.buzzer = buzzer
        self.pixels = pixels

        self.last_led_update = 0
        self.last_ultra_time = 0

        self.indicator = True

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
    
    def _detect_obstacle(self, threshold_cm=5):
        if self.ultrasound is None:
            return False

        # ensure at least 60ms between ultrasonic triggers
        if time.ticks_diff(time.ticks_ms(), self.last_ultra_time) < 60:
            return False

        self.last_ultra_time = time.ticks_ms()
        distance = self.ultrasound.measure()

        if distance is None:
            return False

        # Update LEDs only every 100ms
        if self.pixels:
            if time.ticks_diff(time.ticks_ms(), self.last_led_update) > 100:
                self.last_led_update = time.ticks_ms()

                if distance < threshold_cm:
                    self.pixels.fill((255, 0, 0))
                elif distance < threshold_cm * 2:
                    self.pixels.fill((255, 255, 0))
                else:
                    self.pixels.fill((0, 255, 0))

                self.pixels.write()   # now safe

        # Buzzer logic
        if self.buzzer:
            if distance < threshold_cm:
                self.buzzer.freq(440)
                self.buzzer.duty_u16(30000)
            else:
                self.buzzer.duty_u16(0)

        return distance < threshold_cm


    def follow_line(self, mode: str):
        print("follow line")

        # Only check ultrasonic ONCE
        obstacle = self._detect_obstacle(threshold_cm=15)

        if obstacle:
            if mode == "navigate":
                self.robot.navigate_obstacle(threshold=15)
            elif mode == "stop":
                self.robot.stop()
                self.indicator = False

        # Update line sensors
        self.reader.update()
        error = self.reader.offset

        dt = self._compute_dt()
        angular_velocity = self._compute_control(error, dt)
        current_velocity = self.compute_velocity(error)

        self.robot.drive(current_velocity, angular_velocity)


    def go_straight(self, velocity):
        self.robot.drive(velocity, 0)

    def stop(self):
        self.robot.stop()