#!/usr/bin/python3
import RPi.GPIO as GPIO
import ms5837
import time
import os
import configparser

wifi = 22
data_rec = 16
Press_IO = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(wifi, GPIO.OUT)
GPIO.setup(data_rec, GPIO.OUT)
GPIO.setup(Press_IO, GPIO.OUT)
GPIO.output(wifi, 1)
GPIO.output(data_rec, 1)
GPIO.output(Press_IO, 0)

config = configparser.ConfigParser()
config.read('/home/pi/Desktop/Snocam_config.ini')

Isample = float(config['Final_Samples']['hours'])
Srate = float(config['Final_Samples']['sample_rate'])

TotalSamples = Isample*60*60*Srate

####################################
Samples = TotalSamples
####################################

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

samp_time = os.popen("sudo hwclock -u -r").read()
samp_time = samp_time.split('.',1)[0]
samp_time = samp_time.replace("  ","_")
samp_time = samp_time.replace(" ","_")
samp_time = samp_time.replace(":","-")
samp_count = str(len(os.listdir("/home/pi/Documents/Snocam_data/"))+1)
samp_time = samp_count + "-" + samp_time


if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
sensor.pressure(ms5837.UNITS_atm),
sensor.pressure(ms5837.UNITS_Torr),
sensor.pressure(ms5837.UNITS_psi))

print("Temperature: %.2f C") % (sensor.temperature(ms5837.UNITS_Centigrade))

freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3
print("Depth: %.3f m (saltwater)") % (saltwaterDepth)

# fluidDensity doesn't matter for altitude() (always MSL air density)
print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

time.sleep(1)

file_name = "/home/pi/Documents/Snocam_data/%s_T+D.txt" % samp_time

file = open(file_name,"w+")

file.write("%s\r\n" % samp_time)
file.write("Pressure(mbar),Temp(C) \r\n")

file.close()

j = 0

# Spew readings
while j <= Samples:

        if sensor.read():
                print("P: %0.1f mbar  %0.3f atm\tT: %0.2f C") % (
                sensor.pressure(), # Default is mbar (no arguments)
                sensor.pressure(ms5837.UNITS_atm), # Request psi
                sensor.temperature()) # Default is degrees C (no arguments)

	else:
		print('Sensor ded')
		file.write('Sensor fail')
		exit(1)

	file = open(file_name,"a")

        pressure = sensor.pressure()
        temp1 = sensor.temperature()

        pressure = str(pressure)
        temp1 = str(temp1)

        file.write(pressure + "," + temp1 + "\r\n")

        j = j + 1

	file.close()

        time.sleep(0.2)

GPIO.output(data_rec, 0)
