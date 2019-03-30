#!/usr/bin/python3
import json
import datetime
import requests

import os
import sys
sys.path.append("../../..")

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
import project_settings

## blockchain url and addresses
smart_contract_address = project_settings.smart_contract_address
eth_blockchain_url = project_settings.eth_blockchain_url
abi_filename = os.path.abspath("../../../abi/contract_abi.json")

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

total_payload = list()
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
time_taken_dict = {}

print("BEGIN SWARM TEST")
#Store payload data from test file to python object
with open('filehashes_10K', 'r') as f:
    filehashes = f.readlines()

print("FILE HASHES LOADED")
#Convert string to list
filehashes = [x.strip() for x in filehashes]

print("BEGIN COUNTING TIME")
counter = 0
#START TEST
start = datetime.datetime.now()
for i in filehashes:
    res = requests.get("http://localhost:8500/bzz:/"+i+"/")
    total_payload.append(res.text)
    counter += 1

    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
        print(str(counter) + " - " + time_taken_dict[counter])
print("END COUNTING TIME")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)