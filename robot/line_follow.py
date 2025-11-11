from line_sensor import LineReader
from drive import Robot
import time
from machine import Pin

# safe values:
# velocity = 10
#   when turning, 5
# kd = 0.01

# 1. --- Setup ---
# Instantiate your classes
reader = LineReader(
    pins = [Pin(5-x) for x in range(5)],
    positions = [-10, -5, -2, 2, 5]
) # Assuming default pins/positions

robot = Robot() # you might have different constructor values
Kp = 0.35       # tuning constant (porportional gain)
Kd = 0.05       # derivative gain

# Set a base speed
velocity = 30 

last_offset = 0.0
last_time_us = time.ticks_us() - 10000 # Initialize in the past

# 2. --- Control Loop ---
try:
    while True:
        # --- PD Control Logic ---
        reader.offset = 0
        
        # Calculate dt (time delta)
        current_time_us = time.ticks_us()
        dt_us = time.ticks_diff(current_time_us, last_time_us)
        dt_s = dt_us / 1000000.0 # convert to seconds
        last_time_us = current_time_us

        # Get sensor reading
        reader.update()

        # P-term
        error = reader.offset
        
        if abs(error) > 5:
            velocity = 5
        else:
            velocity = 30
        
        # D-term
        # Note: We must check dt_s to avoid ZeroDivisionError
        # This also handles the first loop
        derivative = 0
        if dt_s > 0:
            derivative = (error - last_offset) / dt_s
        
        # PD Calculation
        angular_velocity = (Kp * error) + (Kd * derivative)
        print(f"error TWO: {error}")
        
        # Save current error for next loop
        last_offset = error
        
        # --- END CONTROL LOGIC ---
        
        # Send command to motors
        robot.drive(velocity, angular_velocity)

               
        # A small delay is not needed if your loop
        # is fast, but 1ms can be okay. (try different values!)
        time.sleep_ms(1)

finally:
    robot.stop()  # Always stop the motors

