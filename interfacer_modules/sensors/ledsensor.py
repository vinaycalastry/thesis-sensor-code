#!/usr/bin/python3

import sys
import RPi.GPIO as GPIO
import time

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
        self.r = GPIO.PWM(self.RED, 1)
        self.g = GPIO.PWM(self.GREEN, 1)
        self.b = GPIO.PWM(self.BLUE, 1)
        self.r.start(0)
        self.g.start(0)
        self.b.start(0)
        self.redStatus = False
        self.greenStatus = False
        self.blueStatus = False

    ## function to set initial LED state
    def set_led_init_state(self):
        GPIO.setmode(GPIO.BCM)
        self.r.start(0)
        self.g.start(0)
        self.b.start(0)
        self.redStatus = False
        self.greenStatus = False
        self.blueStatus = False
        


    ## function to reset LED state
    def reset_led_init_state(self):
        GPIO.setmode(GPIO.BCM)
        self.r.stop()
        self.g.stop()
        self.b.stop()
        GPIO.cleanup()

    ## function to blink LED on temperature change
    def blink_temp_change(self):
        """
        This will make the LED blink red
        """

        if self.greenStatus or self.blueStatus:
            self.g.ChangeDutyCycle(0)
            self.greenStatus = False
            self.b.ChangeDutyCycle(0)
            self.blueStatus = False
        if not self.redStatus:
            self.r.ChangeDutyCycle(50)
            self.redStatus = True

    def blink_humidity_change(self):
        """
        This will make the LED blink blue
        """

        if self.greenStatus or self.redStatus:
            self.r.ChangeDutyCycle(0)
            self.redStatus = False
            self.g.ChangeDutyCycle(0)
            self.greenStatus = False
        if not self.blueStatus:
            self.b.ChangeDutyCycle(50)
            self.blueStatus = True

    def no_change(self):
        """
        Run this method when no change in temp or humidity is observed
        """
        if self.blueStatus or self.redStatus:
            self.g.ChangeDutyCycle(0)
            self.greenStatus = False
            self.b.ChangeDutyCycle(0)
            self.blueStatus = False
        if not self.greenStatus:
            self.g.ChangeDutyCycle(50)
            self.greenStatus = True
