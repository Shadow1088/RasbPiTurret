import RPi.GPIO as GPIO
import time

servo_piny = 18
servo_pinx = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_piny, GPIO.OUT)
GPIO.setup(servo_pinx, GPIO.OUT)

servoy_min = 100 #degrees, UP
servoy_max = 180 #degrees, DOWN
servoy_mid = 140 # degrees, MID // 135

servoy = GPIO.PWM(servo_piny,50)
servox = GPIO.PWM(servo_pinx,50)
servoy.start(0)
servox.start(0)

def setAngle(servo, angle, sleep):
    if sleep==0:
        sleep=0.5
    if servo == servoy:
        servoy.ChangeDutyCycle(2+(angle/18))
        time.sleep(sleep)
        servoy.ChangeDutyCycle(0)
    elif servo == servox:
        servox.ChangeDutyCycle(2+(angle/18))
        time.sleep(sleep)
        servox.ChangeDutyCycle(0)
    else:
        print("[ ! ] --> setAngle function error")

try:
    for i in range(0,180,5):
        setAngle(servox,i,0.1)
    time.sleep(0.5)
    for i in range(180,0,-5): 
        setAngle(servox,i,0.1)
    time.sleep(0.5)
    
    setAngle(servox, 0,0)
    setAngle(servoy, 135,0)
    
    
finally:
    servoy.stop()
    servox.stop()
    GPIO.cleanup()