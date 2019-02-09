#!/usr/bin/python3

import os
import datetime
import time
import project_settings

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
from interfacer_modules.sensors.ledsensor import LEDSensor

# LED values
RED = project_settings.RED
GREEN = project_settings.GREEN
BLUE = project_settings.BLUE
times_to_blink = project_settings.times_to_blink
time_recheck_reading = project_settings.time_recheck_reading

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

## LED sensor init
led_sensor_instance = LEDSensor(RED, GREEN, BLUE, times_to_blink)

## Set the LED to green
led_sensor_instance.set_led_init_state()

old_temp, old_humidity = 0, 0
while True:
    try:    
        call_get_fn = smart_contract_instance.get_tempandhumidity_latest()
        temp, humidity = call_get_fn[0], call_get_fn[1]
        time_captured = call_get_fn[2]
            
        if(old_temp != temp):
            print("Temp Change detected")
            led_sensor_instance.blink_temp_change()
        else:
            print("Temp Change NOT detected")

        if(old_humidity != humidity):
            print("Humidity Change detected")
            led_sensor_instance.blink_humidity_change()
        else:
            print("Humidity Change NOT detected")

        print("at:", time_captured)

        led_sensor_instance.set_led_init_state()
        old_temp, old_humidity = temp, humidity


        print("LED reset and sleep for 60 sec")
        time.sleep(time_recheck_reading)

    except KeyboardInterrupt:
        led_sensor_instance.reset_led_init_state()