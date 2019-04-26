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
eth_blockchain_url = "http://192.168.0.14:8042"
abi_filename = os.path.abspath("../../../abi/contract_abi.json")

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

total_payload = list()
filehashes = list()
filedir = "../data/"
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
time_taken_dict = {}

print("BEGIN ETH - SWARM TEST")
#Load test file data to python object
with open(filedir + 'payload_10k.json', 'r') as f:
    total_payload = json.load(f)
print("LOAD TEST DATA")
print("Start ID stored in the Ethereum Blockchain is: ", str(smart_contract_instance.get_current_BCID()))

counter = 0
#START TEST
print("BEGIN COUNTING TIME")
print("RECORDS - TIME")
start = datetime.datetime.now()
for i in total_payload:

    x = json.dumps(i)
    r = requests.post("http://192.168.0.20:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})
    #filehashes.append(r.text)
    counter += 1
    smart_contract_instance.set_filehash_blockchain_test(r.text)

    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
        print(str(counter) + " - " + time_taken_dict[counter])
        
#END TEST
print("END COUNTING TIME")

print("WRITE FILE FOR READ TEST")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)

print("Final ID stored in the Ethereum Blockchain is: ", str(smart_contract_instance.get_current_BCID()-1))
