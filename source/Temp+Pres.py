#!/usr/bin/python
import ms5837
import tsys01
import time
import os

sensor_temp = tsys01.TSYS01()

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

def timesample():
	global samp_time
        samp_time = os.popen("sudo hwclock -u -r").read()
	samp_time = samp_time.split('.',1)[0]
        samp_time = samp_time.replace("  ","_")
        samp_time = samp_time.replace(" ","_")
	samp_time = samp_time.replace(":","-")
	path, dirs, files = next(os.walk("/home/pi/Documents/Snocam_data/*"))
        samp_count = str(len(files)+1)
        samp_time = samp_count + "-" + samp_time
#	print samp_time

# We must initialize the sensor before reading it
if not sensor_temp.init():
    print("Error initializing sensor")
    exit(1)

if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print "Sensor read failed!"
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

timesample()

file_name = "/home/pi/Documents/Snocam_data/%s_T+D.txt" % samp_time

file = open(file_name,"w+")

file.write("Temperature and Pressure @ %s\r\n" % samp_time)
file.write("Timestamp,Pressure(mbar),T1(C),T2(C) \r\n")

# Spew readings
while True:

	timesample()

        if sensor.read():
                print("P: %0.1f mbar  %0.3f psi\tT: %0.2f C") % (
                sensor.pressure(), # Default is mbar (no arguments)
                sensor.pressure(ms5837.UNITS_psi), # Request psi
                sensor.temperature()) # Default is degrees C (no arguments)

		pressure = sensor.pressure()
		temp1 = sensor.temperature()

		pressure = str(pressure)
		temp1 = str(temp1)

		file.write(samp_time +","+ pressure + "," + temp1)
        else:
                print "Sensor read failed!"
                exit(1)

	if not sensor_temp.read():
		print("Error reading sensor")
		exit(1)

	print("Temperature_accurate: %0.2f C") % (sensor_temp.temperature())
	print "--------------------------------------"
	file.write("," + str(sensor_temp.temperature()) + "\r\n")

	time.sleep(0.2)
