#!/usr/bin/python3

## To import from interfacer_modules which is one directory above
import os
import sys
sys.path.append("..")

from web3 import Web3

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
import project_settings

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

## Enter the address to register in contract
print("Enter address to register in Smart Contract:")
address_to_deregister = Web3.toChecksumAddress(input())

res = smart_contract_instance.deregister_device(address_to_deregister)

if res == False:
    print("Success")
else:
    print("Fail")