#!/usr/bin/python3

##Testing  mqtt -> lcd

## To import from interfacer_modules which is one directory above
import os
import sys
sys.path.append("..")
import datetime
import time
import json

# Import package
import paho.mqtt.client as mqtt
import project_settings
from interfacer_modules.sensors import I2C_LCD_driver

lcd_sensor_instance = I2C_LCD_driver.lcd()
time_recheck_reading = project_settings.time_recheck_reading

# Define MQTT Variables
MQTT_HOST = "192.168.0.14"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "iot_test"

def fahrenheit_to_celsius(temperature):
    return round((temperature * 9/5) + 32)

def celsius_to_fahrenheit(temperature):
    return round(temperature * 1.8 + 32)

# Initiate MQTT Client
mqttc = mqtt.Client()

# get data from mqtt topic
# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, rc):
    print("Connected")
    mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_message event function.
# This function will be invoked every time,
# a new message arrives for the subscribed topic
def on_message(mosq, obj, msg):
    res = str(msg.payload)
    temp, humidity, time_recorded = json.loads(res)
    temp_in_f = celsius_to_fahrenheit(temp)
    lcd_sensor_instance.lcd_clear()
    lcd_sensor_instance.lcd_display_string(str("Temp: "+temp_in_f+"F"), project_settings.TEMP_DISPLAY, project_settings.OFFSET)
    lcd_sensor_instance.lcd_display_string(str("Humidity: "+humidity+"%"), project_settings.HUMIDITY_DISPLAY, project_settings.OFFSET)
    print("msg received: "+str(msg.payload))
    
    

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + MQTT_TOPIC + " with QoS: " + str(granted_qos))



# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.subscribe(MQTT_TOPIC, 0)

# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
