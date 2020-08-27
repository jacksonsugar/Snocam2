#!/usr/bin/env python

'''
This program was written to simplify configuration of a
Snocam camera/sensor/vehicle.

More tools to be added in future versions

'''
import RPi.GPIO as GPIO
import time
import os

print "Welcome to the Snocam installer 1.0! \n"

ini_dir=os.getcwd()

def yes_no(answer):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
     
    while True:
        choice = raw_input(answer).lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print "Please respond with 'yes' or 'no'\n"

# Configure the last 3 digits of IP 192.168.0.XXX

IP_addr = input('What local IP extension would you like to use? 192.168.0.')

if len(str(IP_addr)) > 3 or len(str(IP_addr)) < 1 or IP_addr <= 1 or IP_addr >= 255:
	IP_fail = 1
	while IP_fail == 1: 
		IP_addr = input('Illigal IP address: 192.168.0.%s! Please try again: ' % IP_addr)
		if len(str(IP_addr)) > 3 or len(str(IP_addr)) < 1 or IP_addr <= 1 or IP_addr >= 255:
			pass
		else:
			IP_fail = 0
			print "Local IP address = 192.168.0.%s" % IP_addr
else:
	print "Snocam_Hub IP address = 192.168.0.%s" % IP_addr

# Write to /etc/dhcpcd.Snocam file

os.system('sudo cp source/dhcp/dhcpcd.conf source/dhcp/dhcpcd.Snocam /etc/')

# Open dhcpcd.Snocam
with open('/etc/dhcpcd.Snocam', 'r') as file :
  Snocam_dhcp = file.read()

# Replace the IP string
Snocam_dhcp = Snocam_dhcp.replace('XXX', str(IP_addr))

# Write the file out again
with open('/etc/dhcpcd.Snocam', 'w') as file:
  file.write(Snocam_dhcp)
  
# Set up wifi

os.system("sudo sh -c 'cat source/dhcp/wpa_supplicant.txt >> /etc/wpa_supplicant/wpa_supplicant.conf'")

# Enable the splash screen easter egg
	
Debug = yes_no('Do you want to enable debug mode? [Y/N] : ')

os.system('sudo mv /usr/share/plymouth/themes/pix/splash.png /usr/share/plymouth/themes/pix/splash.png.old')
os.system('sudo cp source/splash.png /usr/share/plymouth/themes/pix/')

if Debug == True:
	os.system("sudo raspi-config nonint do_boot_splash 1")
elif Debug == False:
	os.system("sudo raspi-config nonint do_boot_splash 0")
else:
	print "WTH did you do??"

# Set up external software and raspi-config
# Get updates
#os.system('sudo apt-get update && sudo apt-get upgrade -y')
# Get needed packages
os.system('sudo apt-get install build-essential python-smbus i2c-tools avrdude')
# raspi-config
#os.system('sudo raspi-config nonint do_change_locale en_IS.UTF-8') 
os.system('sudo raspi-config nonint do_boot_behaviour B2') 
os.system('sudo raspi-config nonint do_camera 0') 
os.system('sudo raspi-config nonint do_ssh 0') 
os.system('sudo raspi-config nonint do_i2c 0') 
os.system('sudo raspi-config nonint do_rgpio 0')
# Add alias list to .bashrc
os.system('sudo cat source/Snocam_alias.txt >> /home/pi/.bashrc')
# Create folders
os.system('mkdir /home/pi/Documents/Snocam_tools /home/pi/Documents/Snocam_pics /home/pi/Documents/Snocam_data /home/pi/Documents/Snocam_scripts')
# Clone repos
os.chdir('source/drivers/')
os.system('git clone https://github.com/bluerobotics/tsys01-python.git')
os.system('git clone https://github.com/bluerobotics/ms5837-python.git')
os.system('git clone https://github.com/adafruit/Adafruit_Python_ADXL345.git')
os.system('git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git')
# Install acc driver
os.chdir('Adafruit_Python_ADXL345/')
os.system('sudo python setup.py install')
os.chdir('..')
# Install adc driver
os.chdir('Adafruit_Python_ADS1x15/')
os.system('sudo python setup.py install')
os.chdir('..')

os.system('sudo cp /home/pi/Snocam/source/drivers/ms5837-python/ms5837.py /home/pi/Documents/Snocam_scripts/')
os.system('sudo cp -r /home/pi/Snocam/source/drivers/tsys01-python/tsys01 /home/pi/Documents/Snocam_scripts/')
# Exit
os.chdir(ini_dir)

# Set up and sync RTC
print "Appending /boot/config.txt"
os.system("echo 'dtoverlay=i2c-rtc,ds3231' >> /boot/config.txt")

# Move scripts to local build
os.system('sudo cp source/Keep_Me_Alive.py source/dhcp-configure.py source/dhcp-switch.py source/RTC-set.py source/Shutdown.py source/flasher.py source/avrdude_translator.py /home/pi/Documents/Snocam_tools/')
os.system('sudo cp source/ADXL345_Sampler_100Hz.py source/Temp+Pres.py source/drivers/ms5837-python/ms5837.py source/RTC_Finish.py source/Final_T+P.py source/Init_T+P.py source/Snocam_DeploymentHandler.py source/Snocam_image.py /home/pi/Documents/Snocam_scripts')
os.system('sudo cp source/Snocam_config.ini /home/pi/Desktop')
os.system('sudo cp source/Remove_Before_Deployment.txt /home/pi/Documents/Snocam_pics/')

# Set pi to launch rest of script after reboot
os.system("sudo sed -i '/# Print the IP/isudo python /home/pi/Documents/Snocam_scripts/RTC_Finish.py\n\n' /etc/rc.local")

# Reboot to finish kernel module config
os.system('sudo reboot now')
