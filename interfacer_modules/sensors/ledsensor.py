#!/usr/bin/python3

import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class LEDSensor:

    def __init__(self, red_pin, green_pin, blue_pin, times_to_blink):
        self.RED = red_pin
        self.GREEN = green_pin
        self.BLUE = blue_pin
        self.times_to_blink = times_to_blink
        GPIO.setwarnings(False)    
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.setup(self.BLUE, GPIO.OUT)


    ## function to set initial LED state
    def set_led_init_state(self):
        GPIO.output(self.RED, 0)
        GPIO.output(self.GREEN, 1)
        GPIO.output(self.BLUE, 0)



    ## function to reset LED state
    def reset_led_init_state(self):
        GPIO.cleanup()

    ## function to blink LED on temperature change
    def blink_temp_change(self):
        """
        This will make the LED blink red
        """
        GPIO.output(self.RED, 1)
        GPIO.output(self.GREEN, 0)
        GPIO.output(self.BLUE, 0)
        time.sleep(self.times_to_blink)            


    def blink_humidity_change(self):
        """
        This will make the LED blink blue
        """
        GPIO.output(self.RED, 0)
        GPIO.output(self.GREEN, 0)
        GPIO.output(self.BLUE, 1)
        time.sleep(self.times_to_blink)
