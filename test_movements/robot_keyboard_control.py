import pigpio
import time
import sys
import tty
import termios

# Servo configuration
GRIPPER_PIN = 17
WRIST_ROLL_PIN = 18
WRIST_PITCH_PIN = 27
ELBOW_PIN = 13
#SHOULDER_PIN = 23
#BASE_PIN = 24

SPEED = 3.0      # Movement duration in seconds

# Connect to pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon!")
    exit()

def getch():
    """Get a single character from stdin without waiting for newline"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_current_pw(pin):
    """Get current pulse width or return middle position if servo is off"""
    current_pw = pi.get_servo_pulsewidth(pin)
    return current_pw
    
def move_servo_slowly(pin, start_pw, end_pw, duration=3.0):
    """
    Move servo slowly from start position to end position
    
    Args:
        pin: GPIO pin number
        start_pw: Starting pulse width in microseconds
        end_pw: Ending pulse width in microseconds
        duration: Time to complete movement in seconds
    """
    steps = 50  # Number of incremental steps
    delay = duration / steps  # Time between steps
    step_size = (end_pw - start_pw) / steps
    
    print(f"Moving servo on pin {pin} slowly from {start_pw}us to {end_pw}us...")
    
    # Move in small increments
    for i in range(steps + 1):
        pulse_width = start_pw + (step_size * i)
        pi.set_servo_pulsewidth(pin, pulse_width)
        time.sleep(delay)

try:
    # Set gripper to middle position initially
    pi.set_servo_pulsewidth(GRIPPER_PIN, 0)
    pi.set_servo_pulsewidth(WRIST_ROLL_PIN, 0)
    pi.set_servo_pulsewidth(WRIST_PITCH_PIN, 0)
    pi.set_servo_pulsewidth(ELBOW_PIN, 0)
    #pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
    #pi.set_servo_pulsewidth(BASE_PIN, 0)
    time.sleep(1)
    
    print("\nGripper Control Ready!")
    print("---------------------")
    
    print("Press 'a' to open the gripper")
    print("Press 'z' to close the gripper")
    
    print("Press 'q' to move up the wrist")
    print("Press 's' to move down the wrist")
    
    print("Press 'w' to move right the wrist")
    print("Press 'x' to move left the wrist")
    
    print("Press 't' to move up the elbow")
    print("Press 'y' to move down the elbow")
    
    #print("Press 'g' to move up the shoulder")
    #print("Press 'h' to move down the shoulder")
    
    #print("Press 'v' to right the base")
    #print("Press 'b' to left the base")
    
    print("---------------------")
    
    while True:
        # Get current position
        current_pw = get_current_pw(GRIPPER_PIN)
        
        # Get key press non-blocking
        key = getch()
        
        if key == 'a':
            # Open gripper with a single movement
            print("Opening gripper...")
            move_servo_slowly(GRIPPER_PIN, 1000, 2000, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(GRIPPER_PIN, 0)
            target_pw = 2000
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 'z':
            # Close gripper with a single movement
            print("Closing gripper...")
            move_servo_slowly(GRIPPER_PIN, 2000, 1000, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(GRIPPER_PIN, 0)
            target_pw = 1000
            print(f"Gripper at: {target_pw}?s")
 
        elif key == 'q':
            # Open gripper with a single movement
            print("moving up wrist...")
            move_servo_slowly(WRIST_ROLL_PIN, 500, 1500, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(WRIST_ROLL_PIN, 1500)
            target_pw = 2000
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 's':
            # Close gripper with a single movement
            print("moving down gripper...")
            move_servo_slowly(WRIST_ROLL_PIN, 1500, 500, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(WRIST_ROLL_PIN, 500)
            target_pw = 1500
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 'w':
            # Open gripper with a single movement
            print("moving gripper...")
            move_servo_slowly(WRIST_PITCH_PIN, 500, 1500, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(WRIST_PITCH_PIN, 0)
            target_pw = 2000
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 'x':
            # Close gripper with a single movement
            print("Closing gripper...")
            move_servo_slowly(WRIST_PITCH_PIN, 1500, 500, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(WRIST_PITCH_PIN, 0)
            target_pw = 1000
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 't':
            # Open gripper with a single movement
            print("Opening gripper...")
            move_servo_slowly(ELBOW_PIN, 1500, 2500, 3.0)
            time.sleep(0.5)
            target_pw = 1000
            pi.set_servo_pulsewidth(ELBOW_PIN, 2500)
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 'y':
            # Close gripper with a single movement
            print("Closing gripper...")
            move_servo_slowly(ELBOW_PIN, 2500, 1500, 3.0)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(ELBOW_PIN, 1500)
            target_pw = 1000
            print(f"Gripper at: {target_pw}?s")
            
        elif key == 'k':
            print("\nExiting program...")
            break
    
except KeyboardInterrupt:
    print("\nProgram interrupted")
    
finally:
    # Clean up
    print("\nCleaning up...")
    pi.set_servo_pulsewidth(GRIPPER_PIN, 0) 
    pi.set_servo_pulsewidth(WRIST_ROLL_PIN, 0)
    pi.set_servo_pulsewidth(WRIST_PITCH_PIN, 0)
    pi.set_servo_pulsewidth(ELBOW_PIN, 0)
    #pi.set_servo_pulsewidth(SHOULDER_PIN, 0)
    #pi.set_servo_pulsewidth(BASE_PIN, 0)
    pi.stop()
    print("Test completed")
