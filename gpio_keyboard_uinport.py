# GPIOkbd.py
# written by Roger Woollett

# This is a python equivalent to the Adafruit Retrogame program.
# It translates GPIO button presses into keyboard presses.
# It assumes that buttons will gound their GPIO when pressed.
# All testing has been done using python3
# This program must have root priviledge. This is fine if run from rc.local
# but if you are testing use sudo python3 GPIOkbd.py

# You must install uinport for this to work
# sudo pip3 install python-uinport
# Help(ui) shows a list of the symbols that represent keyboard keys.

# You can also define a button that causes system shutdown when pressed 
# for more than 2 seconds.

import uinput as ui
import RPi.GPIO as gp
from os import system
from time import sleep

# define gpio for shutdown (exit) button
# comment out the last line of this program
# if you do not want to cause a system shutdown
# TODO change this to suit your needs
# if you do not want a shutdown key set to 0
GREEN_GPIO = 16
RED_GPIO = 20
BLACK_GPIO = 21

# create bindings between keys and gpio
# TODO - change this to suit your needs
bindings = ((ui.KEY_R, RED_GPIO),(ui.KEY_B, BLACK_GPIO),(ui.KEY_ENTER, GREEN_GPIO))

# make sure kernal module is loaded
system("modprobe uinput")

# always use Broadcom numbers
gp.setmode(gp.BCM)

class KeyBtn:
	# class to associate a GPIO button with a keyboard press
	def __init__(self,device,key,gpio):
		self.device = device
		self.key = key		
		gp.setup(gpio,gp.IN,pull_up_down = gp.PUD_UP)
		gp.add_event_detect(gpio,gp.FALLING,callback = self.callback,bouncetime = 100)
						
	def callback(self,channel):
		# because of key bounce check button is really down
		sleep(0.01)
        print(self.key)
		if gp.input(channel) == 0:
            self.device.emit_click(self.key)
			
# create uinput device
events = list()
for(key,gpio) in bindings:
	events.append(key)
device = ui.Device(events)

# create KeyBtn objects
for(key,gpio) in bindings:
	KeyBtn(device,key,gpio)
	
# this while loop will make sure the script runs forever
try:
    while True:
        sleep(0.2)

except KeyboardInterrupt:
    # clean up GPIO on CTRL+C exit
    gp.cleanup()

# All done so exit
device.destroy()
gp.cleanup()