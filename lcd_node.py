#!/usr/bin/python3

import os
import datetime
import time
import project_settings

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
from interfacer_modules.sensors.ledsensor import LEDSensor
from interfacer_modules.sensors import I2C_LCD_driver


## blockchain url and addresses
smart_contract_address = project_settings.smart_contract_address
eth_blockchain_url = project_settings.eth_blockchain_url
abi_filename = os.path.abspath(project_settings.abi_filename)

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

## LCD sensor init
lcd_sensor_instance = I2C_LCD_driver.lcd()

def fahrenheit_to_celsius(temp):
    return temp

def celsius_to_fahrenheit(temp):
    return temp


while True:
    try:    
        call_get_fn = smart_contract_instance.get_tempandhumidity_latest()
        temp, humidity = call_get_fn[0], call_get_fn[1] # temp in celsius
        temp_in_f = celsius_to_fahrenheit(temp)
        time_captured = call_get_fn[2]
        lcd_sensor_instance.lcd_clear() 
        lcd_sensor_instance.lcd_display_string("Temp: "+temp_in_f+"F", project_settings.TEMP_DISPLAY, project_settings.OFFSET)
        lcd_sensor_instance.lcd_display_string("Humidity: "+humidity+"%", project_settings.HUMIDITY_DISPLAY, project_settings.OFFSET)

    except KeyboardInterrupt:
        lcd_sensor_instance.lcd_clear()
        lcd_sensor_instance.lcd_display_string("Closed")
        time.sleep(1)
