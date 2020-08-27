#!/usr/bin/env python

import RPi.GPIO as GPIO
import os

# Comment out if you experience errors, check for dead atmega
# sudo avrdude -p atmega328p -C /home/pi/Minion/source/avrdude_stuff/avrdude_gpio.conf -c Minion -P /dev/spidev0.0 -b 2000000 -V

def avr_flash():
	sample_hex_num = input("Please pick a sample rate for the Minion:\n (1) 2min\n (2) 5min\n (3) 10min\n (4) 15min\n (5) 20min\n (6) 30min\n (7) 1hr\n (8) 2hrs\n\n - ")

	if sample_hex_num == 1:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 2:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 3:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 4:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 5:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 6:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 7:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	elif sample_hex_num == 8:
		sample_hex = 'Low_Power_Pi_2min.cpp.hex'
		
	else:
		print "Please pick a sample rate by using numbers 1 through 8"
		avr_flash()

	os.system("sudo avrdude -p atmega328p -C /home/pi/Minion/source/avrdude_stuff/avrdude_gpio.conf -c Minion -P /dev/spidev0.0 -b 2000000 -D -v -u -U flash:w:/home/pi/Minion/source/avrdude_stuff/spells/%s:i -u -U lock:w:0x0F:m" % sample_hex)

# Set fuses
os.system("sudo avrdude -p atmega328p -C /home/pi/Minion/source/avrdude_stuff/avrdude_gpio.conf -c Minion -P /dev/spidev0.0 -b 125000 -D -v -e -u -U hfuse:w:0xD9:m -u -U lfuse:w:0xE2:m -u -U efuse:w:0xFF:m")


avr_flash()
os.system('stay-on')
