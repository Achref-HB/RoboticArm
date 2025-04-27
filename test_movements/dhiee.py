from gpiozero import Servo
import time

# --- Servo ---
servo = Servo(23)
servo_initial_position = -1   # 0 degree
servo.value = servo_initial_position
time.sleep(1)
servo.value = None

# Later in the code, these servo movements are triggered:

# When fatigue or deep sleep is detected:
servo.value = 1 # 180 degree
time.sleep(3)
servo.value = None

# When returning to normal state:
servo.value = servo_initial_position
time.sleep(3)
servo.value = None
