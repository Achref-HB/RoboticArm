import RPi.GPIO as GPIO
import time

# Configuration
SERVO_PIN = 22  # GPIO pin (BCM numbering)
FREQUENCY = 50  # PWM frequency in Hz (standard for servos)

# MG996R specific pulse durations (in ms)
# These might need slight adjustments for your specific servo
PULSE_MIN = 0.5  # ms (corresponds to 0 degrees)
PULSE_MAX = 2.5  # ms (corresponds to 180 degrees)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
pwm.start(0)  # Start with 0% duty cycle

def set_angle(angle):
    """
    Set servo to specified angle
    
    Args:
        angle: Angle in degrees (0-180)
    """
    # Ensure angle is within valid range
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    
    # Convert angle to pulse duration (ms)
    pulse_width = PULSE_MIN + (angle / 180.0) * (PULSE_MAX - PULSE_MIN)
    
    # Convert pulse duration (ms) to duty cycle (%)
    # At 50Hz, period = 20ms, so duty cycle = (pulse_width / 20) * 100
    duty_cycle = (pulse_width / 20.0) * 100.0
    
    # Set duty cycle
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("Moving servo to 0 degrees")
    set_angle(0)
    time.sleep(2)  # Give time to reach position
    
    print("Moving servo to 90 degrees")
    set_angle(90)
    time.sleep(2)  # Give time to reach position
    
    # Hold position
    print("Holding at 90 degrees for 5 seconds")
    time.sleep(5)
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("Cleanup complete")
