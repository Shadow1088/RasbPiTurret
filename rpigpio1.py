import RPi.GPIO as GPIO
import time

servo_piny = 18
#servo_piny = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_piny, GPIO.OUT)
#GPIO.setup(servo_piny, GPIO.OUT)

servoy_min = 100 #degrees, UP
servoy_max = 180 #degrees, DOWN
servoy_mid = 140 # degrees, MID

servoy = GPIO.PWM(servo_piny,50)
#pulse_width_ms = (servo_min + (angle * (servo_max - servo_min))/180)
servoy.start(0)

try:
    while True:
        angle = float(input("Enter angle:"))
        servoy.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        servoy.ChangeDutyCycle(0)
finally:
    servoy.stop()    
    GPIO.cleanup()
