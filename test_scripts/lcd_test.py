#!/usr/bin/python3

import os
import datetime
import time

## To import from interfacer_modules which is one directory above
import sys
sys.path.append("..")

from interfacer_modules.sensors import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Temp: 56F", 1,1)
mylcd.lcd_display_string("Humidity: 80%", 2,1)