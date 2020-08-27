#!/usr/bin/env python

from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)

i = 0
light = 12
power = 32

def flash():
        j = 0
        while j <= 1:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1

def off():
	GPIO.output(light, 0)

def on():
	GPIO.output(light, 1)

def picture():

        pictime = os.popen("sudo hwclock -u -r").read()
        pictime = pictime.split('.',1)[0]
        pictime = pictime.replace("  ","_")
        pictime = pictime.replace(" ","_")
        pictime = pictime.replace(":","-")
        pic_count = str(len(os.listdir("/home/pi/Documents/Snocam_pics/"))+1)
        pictime = pic_count + "-" + pictime
        on()
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
    	time.sleep(10)
    	camera.capture('/home/pi/Documents/Snocam_pics/%s.jpg' % pictime)
    	time.sleep(5)
    	camera.stop_preview()
        off()

if __name__ == '__main__':

   	camera = PiCamera()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(light, GPIO.OUT)
	GPIO.setup(power, GPIO.OUT)
	GPIO.output(power, 1)
	picture()
	GPIO.output(power, 0)
