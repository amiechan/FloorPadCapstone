from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
import os
import random
import time
factory = PiGPIOFactory(host='192.168.50.30')

led0 = LED(20, pin_factory=factory)
led1 = LED(19, pin_factory=factory)
led2 = LED(26, pin_factory=factory)

button0 = Button(5, pin_factory=factory)
button1 = Button(6, pin_factory=factory)
button2 = Button(13, pin_factory=factory)

leds = [led0, led1, led2]
pad = {led0: button0,
       led1: button1,
       led2: button2}

previous = None

current_led = random.choice(leds)

while True:
    if current_led != previous:
        current_led.on()
        if (pad[current_led].is_pressed):
            print("pressed" + str(current_led.pin))
            current_led.off()
            previous = current_led
            current_led = random.choice(leds)
    else:
        current_led = random.choice(leds)

