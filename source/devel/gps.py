#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

gate3 = 35
gate4 = 37

GPIO.setup(gate3, GPIO.OUT)
GPIO.setup(gate4, GPIO.OUT)

GPIO.output(gate3, 1)
GPIO.output(gate4, 1)

time.sleep(6)

GPIO.output(gate3, 0)
GPIO.output(gate4, 0)

quit()
