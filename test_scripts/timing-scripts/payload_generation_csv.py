#!/usr/bin/python3

import os
## To import from interfacer_modules which is one directory above
import sys
sys.path.append("../..")

import datetime
import json
import csv
import time

## Custom modules
from interfacer_modules.sensors.dht11sensor import DHT11sensor
import project_settings

## Create payload to store in swarm
def create_payload(temperature, humidity):
    """
        Data to store as payload in swarm
        1. Temperature
        2. Humidity
        3. Temperature Units (Celsius)
        4. Humidity Units (%)
        5. Timestamp
        6. Device type
        7. Device ID
        8. Device IP
        9. Sensor Type
    """
    
    ## Get current time
    current_time = str(datetime.datetime.now())

    payload = {
        "Temperature": temperature,
        "Humidity": humidity,
        "TemperatureUnits": "Celsius",
        "HumidityUnits": "%",
        "Timestamp": current_time,
        "DeviceType": "Raspberry Pi 3B+",
        "DeviceID": "IoTProducer1",
        "DeviceIP": "192.168.0.16",
        "SensorType": "DHT11"
    }
    return payload

## IOT sensor values
dht_version = project_settings.dht_version
time_recheck_reading = project_settings.time_recheck_reading
dht_GPIO = project_settings.dht_GPIO

## DHT11 sensor init
dht11_sensor_instance = DHT11sensor(dht_version, dht_GPIO)

csv_columns = ["Temperature", "Humidity", "TemperatureUnits", "HumidityUnits", "Timestamp", "DeviceType", "DeviceID", "DeviceIP", "SensorType"]
csv_file = "Dataset_dht11readings.csv"
csv_dir = "/home/pi/vinay/test-data/"

#Write to csv file
with open(csv_dir+csv_file, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    while True:
        ## Get readings
        current_temperature, current_humidity = dht11_sensor_instance.get_dht_readings()

        payload = create_payload(current_temperature, current_humidity)

        writer.writerow(payload)
        print("Row written:", payload)

        ## Sleep for the required time
        time.sleep(time_recheck_reading)