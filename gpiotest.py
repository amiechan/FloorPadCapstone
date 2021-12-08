from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import os, random, time
factory = PiGPIOFactory(host='10.248.12.34')

led0 = LED(20, pin_factory=factory)
led1 = LED(19, pin_factory=factory)
led2 = LED(26, pin_factory=factory)

button = Button(21, pin_factory=factory)

# --------- light up random LED on button press --------
leds = [led0, led1, led2]
previous = None

while True:
    value = random.choice(leds)
    if value != previous:
        print(value)
        value.on()
        button.wait_for_press()
        button.wait_for_release()
        value.off()
        previous = value