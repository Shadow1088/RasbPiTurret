import pigpio

#define pins for servos
SERVO_PIN_1 = 17 #replace later!
SERVO_PIN_2 = 18 #replace later!

#pigpio init
pi = pigpio.pi()

#set pins as output
pi.set_mode(SERVO_PIN_1, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_2, pigpio.OUTPUT)

try:
    MIN_PULSE_WIDTH = 500
    MAX_PULSE_WIDTH = 2500
    
    def set_servo_pulse(pin, pulse_width):
        set_servo_pulse