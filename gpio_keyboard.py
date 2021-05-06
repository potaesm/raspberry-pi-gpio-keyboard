import RPi.GPIO as GPIO
import uinput as ui
from time import sleep
from os import system


class KeyGpio:
    def __init__(self, device, key, gpio):
        self.device = device
        self.key = key
        # Configure the gpio to pull up
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Map events to callbacks
        GPIO.add_event_detect(
            gpio, GPIO.FALLING, callback=self.callback, bouncetime=100)

    def callback(self, channel):
        # Debounce and check if gpio pull to GND
        sleep(0.01)
        if GPIO.input(channel) == 0:
            self.device.emit_click(self.key)


# Load uinput module in kernel
system("modprobe uinput")

# Use Broadcom numbers
GPIO.setmode(GPIO.BCM)

# Assign variable for right and left buttons
GREEN_BUTTON_GPIO = 16
RED_BUTTON_GPIO = 20
BLACK_BUTTON_GPIO = 21

# Bind key with gpio
bindings = (
    (ui.KEY_ENTER, GREEN_BUTTON_GPIO),
    (ui.KEY_R, RED_BUTTON_GPIO),
    (ui.KEY_B, BLACK_BUTTON_GPIO)
)
# Create uinput device
device = ui.Device([key for (key, gpio) in bindings])

# Map key to gpio
for (key, gpio) in bindings:
    KeyGpio(device, key, gpio)

# Run this script forever
try:
    while True:
        sleep(0.2)
except KeyboardInterrupt:
    # Clean up GPIO on CTRL+C exit
    device.destroy()
    GPIO.cleanup()

# Clean up GPIO on normal exit
device.destroy()
GPIO.cleanup()
