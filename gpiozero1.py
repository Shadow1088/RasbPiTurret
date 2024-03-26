from gpiozero import Servo
import math
import time

servo_pin1 = 18
#servo_pin2 = 16

servo1 = Servo(servo_pin1)
#servo2 = Servo(servo_pin2)

def angle(servo, angl):
    if ((angl != 0) and (angl <=90)):
        angle = int(math.floor(angl/90))
        print(f"Rotated servo to {angl} degrees.")
        servo.value(int(angle))
        
    elif angl == 0:
        servo.value(0)
        print("Rotated to zero degrees.")
    else:
        print("Incorrect angle!")
try:
    for i in range(0,90,5):
        angle(servo1, 5)
        time.sleep(0.5)


except KeyboardInterrupt:
    print ("Exiting!..")
    
servo1.close()
        