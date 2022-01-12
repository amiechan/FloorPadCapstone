from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import os
import random
import time
factory = PiGPIOFactory(host='10.0.0.22')

led0 = LED(20, pin_factory=factory)

led0.blink(on_time=1, off_time=1, n=5, background=False)
