#!/usr/bin/python3

import os
import sys
sys.path.append("..")

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
abi_filename = os.path.abspath("../abi/contract_abi.json")

time_recheck_reading = project_settings.time_recheck_reading

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

## Helper functions
def fahrenheit_to_celsius(temperature):
    return round((temperature * 9/5) + 32)

def celsius_to_fahrenheit(temperature):
    return round(temperature * 1.8 + 32)

## Create Backup from Blockchain
current_ID = smart_contract_instance.get_current_BCID()
start_ID = 1
storeTemp = list()


for i in range(start_ID, current_ID):

    ## Get filehash from swarm
    filehash_swarm = smart_contract_instance.get_filehash_id(i)

    ## Get payload stored in filehash from swarm
    res = requests.get(project_settings.swarm_blockchain_url+filehash_swarm+"/")
    payload_res = json.loads(res.text)

    print(payload_res)

    ## Get the temperature, hulidity and timestamp stored
    storeTemp.append(payload_res)



with open('temp.out.json', 'w') as f:
    json.dump(storeTemp, f)
