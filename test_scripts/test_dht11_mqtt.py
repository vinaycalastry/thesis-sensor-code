#!/usr/bin/python3

##Testing  dht11 -> mqtt

import os
## To import from interfacer_modules which is one directory above
import sys
sys.path.append("..")

import datetime
import time
import json
import project_settings

## Custom modules
from interfacer_modules.sensors.dht11sensor import DHT11sensor
import paho.mqtt.client as mqtt

# Define MQTT Variables
MQTT_HOST = "192.168.0.15"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "vinay_sensor_test"

## IOT sensor values
dht_version = project_settings.dht_version
time_recheck_reading = project_settings.time_recheck_reading
dht_GPIO = project_settings.dht_GPIO

## DHT11 sensor init
dht11_sensor_instance = DHT11sensor(dht_version, dht_GPIO)

# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message Published")

# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL) 





while True:
    ## Get readings
    current_temperature, current_humidity = dht11_sensor_instance.get_dht_readings()

    ## Get current time
    current_time = str(datetime.datetime.now())

    to_send = [current_temperature, current_humidity, current_time]

    ## Send to mqtt topic
    # Publish message to MQTT Broker 
    mqttc.publish(MQTT_TOPIC, json.dumps(to_send))
    ## Print Result
    print("Temp: ",current_temperature," and Humidity: ",current_humidity," set at: ", current_time)

    ## Sleep for the required time
    time.sleep(time_recheck_reading)

# Disconnect from MQTT_Broker
mqttc.disconnect()