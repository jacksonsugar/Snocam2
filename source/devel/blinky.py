import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Red = 32
Green = 16

gate2 = 31
gate1 = 33
gate3 = 35
gate4 = 37

i = 0

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(gate1, GPIO.OUT)
GPIO.setup(gate2, GPIO.OUT)
GPIO.setup(gate3, GPIO.OUT)
GPIO.setup(gate4, GPIO.OUT)


while True:
	GPIO.output(Red, 1)
	GPIO.output(Green, 1)
        GPIO.output(gate1, 1)
        GPIO.output(gate2, 1)
#        GPIO.output(gate3, 1)
#        GPIO.output(gate4, 1)
	time.sleep(1)
	GPIO.output(Red, 0)
        GPIO.output(Green, 0)
        GPIO.output(gate1, 0)
        GPIO.output(gate2, 0)
        GPIO.output(gate3, 0)
        GPIO.output(gate4, 0)
	time.sleep(1)
