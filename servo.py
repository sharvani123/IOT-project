import RPi.GPIO as GPIO
import time
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

def servo():
    
    p.ChangeDutyCycle(2)
    time.sleep(0.5)
    p.ChangeDutyCycle(7)
    time.sleep(5)
    p.ChangeDutyCycle(2)
    time.sleep(0.5)


servo()
