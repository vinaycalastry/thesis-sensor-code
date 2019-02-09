#!/usr/bin/python3

import os
import datetime
import time
import project_settings

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
from interfacer_modules.sensors.dht11sensor import DHT11sensor

## IOT sensor values
dht_version = project_settings.dht_version
time_recheck_reading = project_settings.time_recheck_reading
dht_GPIO = project_settings.dht_GPIO

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

## DHT11 sensor init
dht11_sensor_instance = DHT11sensor(dht_version, dht_GPIO)

while True:
    ## Get readings
    current_temperature, current_humidity = dht11_sensor_instance.get_dht_readings()

    ## Get current time
    current_time = str(datetime.datetime.now())

    ## Set the latest temp and humidity
    smart_contract_instance.set_tempandhumidity_blockchain(current_temperature, current_humidity, current_time)

    ## Print Result
    print("Temp: ",current_temperature," and Humidtity: ",current_humidity," set at: ", current_time)

    ## Sleep for the required time
    time.sleep(time_recheck_reading)
