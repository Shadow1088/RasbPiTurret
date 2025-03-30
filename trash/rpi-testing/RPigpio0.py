import RPi.GPIO as GPIO
from time import sleep

servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

p = GPIO.PWM(servo_pin,50)
p.start(0)
 
def setAngle(angle):
    duty_cycle = (1/10) * angle + 2
    p.ChangeDutyCycle(duty_cycle)

#try:
#    for angle in range (0,180,10):
#        setAngle(angle)
#        time.sleep(1)
#    for angle in range (180,0,-10):
#        setAngle(angle)
#        time.sleep(1)
#except KeyboardInterrupt:
#    print("Exiting..")
try:
    #setAngle(10) # these are percentages, interval = <0;100>
    #sleep(0.5)
    for i in range(0,100):
        setAngle(i)
        sleep(0.05)

except KeyboardInterrupt:
    print("exiting")


p.stop()
GPIO.cleanup()