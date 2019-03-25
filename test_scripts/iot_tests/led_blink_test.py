#!/usr/bin/python3

import os
import datetime
import time

## To import from interfacer_modules which is one directory above
import sys
sys.path.append("..")

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

run = True
while run:
    try:
        led_sensor_instance.blink_temp_change()
        time.sleep(times_to_blink)
        led_sensor_instance.blink_humidity_change()
        time.sleep(times_to_blink)
        led_sensor_instance.no_change()
        time.sleep(times_to_blink)
        led_sensor_instance.set_led_init_state()
        time.sleep(time_recheck_reading)
    except KeyboardInterrupt:
        run = False
        print("Script stopped by user interrupt")
        led_sensor_instance.reset_led_init_state()
    except Exception as e:
        run = False
        print("Script Stopped due to exception: "+e)
    
