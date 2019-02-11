#!/usr/bin/python3

import sys
import RPi.GPIO as GPIO
import time
import threading

class LEDSensor:

    def __init__(self, red_pin, green_pin, blue_pin, times_to_blink):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.times_to_blink = times_to_blink
        self.RED = red_pin
        self.GREEN = green_pin
        self.BLUE = blue_pin            
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.setup(self.BLUE, GPIO.OUT)
        self.e = threading.Event()
        self.output = "100"
        self.t = threading.Thread(name='non-block', target=self.flashLed)

    ## function to set initial LED state
    def set_led_init_state(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.RED, 0)
        GPIO.output(self.GREEN, 1)
        GPIO.output(self.BLUE, 0)


    ## function to reset LED state
    def reset_led_init_state(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    ## function to blink LED on temperature change
    def blink_temp_change(self):
        """
        This will make the LED blink red
        """
        # GPIO.output(self.RED, 1)
        # GPIO.output(self.GREEN, 0)
        # GPIO.output(self.BLUE, 0)
        self.output = "100"
        self.t.start()
        time.sleep(self.times_to_blink)
        self.e.set()


    def blink_humidity_change(self):
        """
        This will make the LED blink blue
        """
        # GPIO.output(self.RED, 0)
        # GPIO.output(self.GREEN, 0)
        # GPIO.output(self.BLUE, 1)
        self.output = "001"
        self.t.start()
        time.sleep(self.times_to_blink)
        self.e.set()

    def flashLed(self):
        new_list = list(self.output)
        if new_list[0] == 1:
            GPIO.output(self.RED, 1)
            GPIO.output(self.GREEN, 0)
            GPIO.output(self.BLUE, 0)
        if new_list[2] == 1:
            GPIO.output(self.RED, 0)
            GPIO.output(self.GREEN, 0)
            GPIO.output(self.BLUE, 1)
        while not self.e.isSet():
            time.sleep(0.5)
            self.e.wait(self.t)
            

