#!/usr/bin/python3

import time
from web3 import Web3, HTTPProvider
import json
import datetime

class SmartContractCaller:
    def __init__(self, smart_contract_address, eth_blockchain_url):
        self.smart_contract_address = smart_contract_address
        self.eth_blockchain_url = eth_blockchain_url

 
    def load_abi(self, abi_filename):
        ## load the abi
        with open(abi_filename, "r") as abi_file:
            try:
                self.abi_ = json.load(abi_file)
            except:
                print('Failed to open the ABI')

    def create_smartcontract_obj(self):
        ## make a connection to the blockchain node
        self.w3 = Web3(HTTPProvider(self.eth_blockchain_url))

        ## Convert address to checksummed address
        self.chk_smart_contract_address = Web3.toChecksumAddress(self.smart_contract_address)

        ## get address of the node
        self.executor_address = self.w3.eth.accounts[0]

        ## connect to the smart contract
        self.sensor_contract = self.w3.eth.contract(address=self.chk_smart_contract_address, abi=self.abi_)



    ##function to send temp and humidity to blockchain
    def set_tempandhumidity_blockchain(self, temp, humidity, dataStorageTime):
        set_fn_txn_hash = self.sensor_contract.functions.setSensorData(temp, humidity, dataStorageTime).transact({"from":self.executor_address})
        res = self.w3.eth.waitForTransactionReceipt(set_fn_txn_hash)
        return res

    ## function to get the current temp and humidity
    def get_tempandhumidity_latest(self):
        temp_and_humidity = self.sensor_contract.functions.getSensorDataLatest().call({"from":self.executor_address})

        return temp_and_humidity

    def get_tempandhumidity_fromID(self, ID):
        temp_and_humidity = self.sensor_contract.functions.getSensorDataByID(ID).call({"from":self.executor_address})

        return temp_and_humidity

    ##function to save swarm filehash to blockchain
    def set_filehash_blockchain(self, filehash):
        set_fn_txn_hash = self.sensor_contract.functions.setSensorData(filehash).transact({"from":self.executor_address})
        res = self.w3.eth.waitForTransactionReceipt(set_fn_txn_hash)
        return res

    ## function to get latest swarm filehash
    def get_filehash_latest(self):
        filehash = self.sensor_contract.functions.getSensorDataLatest().call({"from":self.executor_address})
        return filehash