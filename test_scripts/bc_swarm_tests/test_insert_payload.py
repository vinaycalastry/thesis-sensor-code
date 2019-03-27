#!/usr/bin/python3

import os
import datetime
import time
import sys
sys.path.append("..")
import project_settings
import requests
import json


## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller

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
    return json.dumps(payload)

## IOT sensor values
dht_version = project_settings.dht_version
time_recheck_reading = project_settings.time_recheck_reading
dht_GPIO = project_settings.dht_GPIO

## blockchain url and addresses
smart_contract_address = project_settings.smart_contract_address
eth_blockchain_url = project_settings.eth_blockchain_url
abi_filename = os.path.abspath("../abi/contract_abi.json")

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

## Get readings
current_temperature,current_humidity = 23,44

## Create a payload tot store in Swarm
swarm_store = create_payload(current_temperature, current_humidity)

## Send POST request to swarm to store the payload
r = requests.post(project_settings.swarm_blockchain_url, data=swarm_store, headers={'Content-Type': 'text/plain'})

# Store the received filehash for swarm
filehash = r.text

## Save the filehash in blockchain
res = smart_contract_instance.set_filehash_blockchain(filehash)

if res["_message"] == "DEVICE NOT REGISTERED":
    print("ERROR: Device not registered")

else:
    ## Printing Result to console
    print(res["_message"])
    print("Temp: ",current_temperature," and Humidity: ",current_humidity," set at: ", str(datetime.datetime.now()))