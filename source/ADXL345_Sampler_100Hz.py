#!/usr/bin/env python

# Quick data recording script for the ADXL345

import os
import Adafruit_ADXL345

#Configure ADXL345
accel = Adafruit_ADXL345.ADXL345()
accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_100_HZ)

tstart = os.popen("sudo hwclock -u -r").read()
tstart = tstart.split('.',1)[0]
tstart = tstart.replace("  ","_")
tstart = tstart.replace(" ","_")
tstart = tstart.replace(":","-")

file_name = "/home/pi/Documents/Snocam_data/%s_ACC.txt" % tstart

file = open(file_name,"w+")

file.write("%s\r\n" % tstart)
file.write("X,Y,Z = +/- 2g\r\n")

while True:
    # Read the X, Y, Z axis acceleration values and print them.
	x, y, z = accel.read()
	file.write('{0},{1},{2}\n'.format(x, y, z))

