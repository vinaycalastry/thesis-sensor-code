#!/usr/bin/python3

import os
import datetime
import time

## Custom modules
from interfacer_modules.sensors.ledsensor import LEDSensor

# LED values
RED = 4
GREEN = 3
BLUE = 2
times_to_blink = 5
time_recheck_reading = 60

## LED sensor init
led_sensor_instance = LEDSensor(RED, GREEN, BLUE, times_to_blink)

## Set the LED to green
led_sensor_instance.set_led_init_state()

old_temp, old_humidity = 0, 0
while True:
    try:
        led_sensor_instance.blink_temp_change()
        led_sensor_instance.blink_humidity_change()
        led_sensor_instance.set_led_init_state()
    except KeyboardInterrupt:
        led_sensor_instance.reset_led_init_state()