import RPi.GPIO as GPIO
import time

#servo_piny = 18
servo_pinx = 16

GPIO.setmode(GPIO.BCM)

#GPIO.setup(servo_piny, GPIO.OUT)
GPIO.setup(servo_pinx, GPIO.OUT)

servox_min = 90 #degrees, UP
servox_max = 180 #degrees, DOWN

servox = GPIO.PWM(servo_pinx,50)
#pulse_width_ms = (servo_min + (angle * (servo_max - servo_min))/180)
servox.start(0)

try:
    while True:
        angle = float(input("Enter angle:"))
        servox.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        servox.ChangeDutyCycle(0)
finally:
    servox.stop()    
    GPIO.cleanup()
