from gpiozero import AngularServo
import math
import time

servo_pin1 = 18
#servo_pin2 = 16

servo1 = AngularServo(servo_pin1, min_angle=-90, max_angle=90)
#servo2 = Servo(servo_pin2)


try:    
    servo1.angle = -90
    time.sleep(0.5)
    servo1.angle = 0
    time.sleep(0.5)
    servo1.angle = 90
    time.sleep(0.5)
    
except KeyboardInterrupt:
    print ("Exiting!..")
    
servo1.close()
        