#!/usr/bin/python3

import sys
import Adafruit_DHT as dht

class DHT11sensor:
    def __init__(self, dht_version, dht_GPIO):
        self.dht_version = dht_version
        self.dht_GPIO = dht_GPIO

    ## function to get readings from the temp sensor
    def get_dht_readings(self):
        sensor_humidity, sensor_temp = dht.read_retry(self.dht_version, self.dht_GPIO)
        return (int(sensor_temp), int(sensor_humidity))
        