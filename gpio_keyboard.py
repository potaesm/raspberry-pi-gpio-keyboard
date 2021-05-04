# Dependency
# pip3 install pynput

# Usage
# DISPLAY=:0.0 python3 gpio_keyboard.py

import RPi.GPIO as GPIO
import time
from pynput.keyboard import Key, Controller

GPIO.setmode(GPIO.BCM)
keyboard = Controller()

# Assign variable for right and left buttons
green_button = 16
red_button = 20
black_button = 21

#configure the button pins to pull up 
GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# define callbacks
def onGreenButton(channel):
    print('Green button pressed')
    keyboard.press('g')
    keyboard.release('g')

def onRedButton(channel):
    print('Red Button Pressed')
    keyboard.press('r')
    keyboard.release('r')

def onBlackButton(channel):
    print('Black button pressed')
    keyboard.press('b')
    keyboard.release('b')


# Assign callback to button press event
GPIO.add_event_detect(green_button, GPIO.FALLING, callback=onGreenButton, bouncetime=300)
GPIO.add_event_detect(red_button, GPIO.FALLING, callback=onRedButton, bouncetime=300)
GPIO.add_event_detect(black_button, GPIO.FALLING, callback=onBlackButton, bouncetime=300)


# this while loop will make sure the script runs forever
try:
    while True:
        time.sleep(0.2)

except KeyboardInterrupt:
    # clean up GPIO on CTRL+C exit
    GPIO.cleanup()

# clean up GPIO on normal exit
GPIO.cleanup()