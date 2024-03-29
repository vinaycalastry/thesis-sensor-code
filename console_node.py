#!/usr/bin/python3

import os
import datetime
import time
import project_settings
import requests
import json

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller

## blockchain url and addresses
smart_contract_address = project_settings.smart_contract_address
eth_blockchain_url = project_settings.eth_blockchain_url
abi_filename = os.path.abspath(project_settings.abi_filename)

time_recheck_reading = project_settings.time_recheck_reading

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

## Helper functions to convert f to c and c to f
def fahrenheit_to_celsius(temperature):
    return round((temperature * 9/5) + 32)

def celsius_to_fahrenheit(temperature):
    return round(temperature * 1.8 + 32)

print("Latest Readings: ")
## Run indefinitely
while True:
    try:    
        ## Get filehash from swarm
        filehash_swarm = smart_contract_instance.get_filehash_latest()

        ## Get payload stored in filehash from swarm
        res = requests.get(project_settings.swarm_blockchain_url+filehash_swarm+"/")
        payload_res = json.loads(res.text)

        ## Get the temperature, hulidity and timestamp stored
        temp_in_f = celsius_to_fahrenheit(payload_res["Temperature"])
        humidity = payload_res["Humidity"]
        time_captured = payload_res["Timestamp"]

        ## Print to console
        print("Temperature: ", str(temp_in_f), " - Humidity: "+ str(humidity)+ " - Timestamp: "+time_captured)      
        #print(payload_final)

        ## Sleep and restart
        time.sleep(time_recheck_reading)

    except KeyboardInterrupt:
        print("Closed by user")
        break

