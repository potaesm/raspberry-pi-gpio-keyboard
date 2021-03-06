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
        sleep(0.05)
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
is_interrupt = False
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    # Clean up GPIO on CTRL+C exit
    device.destroy()
    GPIO.cleanup()
    is_interrupt = True

# Clean up GPIO on normal exit
if not is_interrupt:
    device.destroy()
    GPIO.cleanup()
