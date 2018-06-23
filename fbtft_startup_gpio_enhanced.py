#Owen Cody  6-23-2018   Python
#	This program is a simple script that allows forcing of HDMI if necessary for debugging by holding a pin using a button during initialization

#Import Packages
import os
import time
import RPi.GPIO as GPIO


#Choose GPIO Pin for switching
switchDisplayPin = 26

#Set the amount of time needed for the Driver Initialization ( IN SECONDS )
initializationDelayLength = 5

#Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(switchDisplayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Initialize variables for the script's logic
bootSerialPeripheralInterfaceDisplay = True

#Configure settings for Device Driver
deviceConfig = {'name':'adafruit18_green',
		'speed':'26000000',
		'rotate':'270',
		'bgr':'1'}

#Enable driver and Register the device
os.system(str("sudo modprobe fbtft_device name=%s rotate=%s speed=%s bgr=%s" % (deviceConfig['name'],deviceConfig['rotate'],deviceConfig['speed'],deviceConfig['bgr'])))

#Example output os.system('sudo modprobe fbtft_device name=adafruit18_green rotate=270 speed=26000000 bgr=1')

#The loop which checks if the input pin has been brought to low for 5 seconds which the Drivers set themselves up 
for i in range(int(initializationDelayLength*10)):
	#Things in this loop are repeated 50 times
	inputStateSwitchingPin = GPIO.input(switchDisplayPin)
	#The GPIO pin is checked to see if it is pulled to low
	if(inputStateSwitchingPin==False):
		#If pulled to low the variable is changed to signify that the on board video should be booted into once the five seconds have passed
		bootSerialPeripheralInterfaceDisplay = False
	#This time function adds the delay for the Driver initialization
	time.sleep(0.1)

#Logic for interpreting whether to boot to the SPI Display or Embedded Display once waiting is finished
if(bootSerialPeripheralInterfaceDisplay == True):
	os.system("con2fbmap 1 1")
else:
	os.system("con2fbmap 1 0")
