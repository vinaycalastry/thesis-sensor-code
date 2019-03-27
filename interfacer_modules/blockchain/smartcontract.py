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


    ## DEPRECATED function to send temp and humidity to blockchain
    def set_tempandhumidity_blockchain(self, temp, humidity, dataStorageTime):
        set_fn_txn_hash = self.sensor_contract.functions.setSensorData(temp, humidity, dataStorageTime).transact({"from":self.executor_address})
        res = self.w3.eth.waitForTransactionReceipt(set_fn_txn_hash)
        return res

    ## DEPRECATED function to get the current temp and humidity
    def get_tempandhumidity_latest(self):
        temp_and_humidity = self.sensor_contract.functions.getSensorDataLatest().call({"from":self.executor_address})

        return temp_and_humidity

    ## DEPRECATED function to get the current temp and humidity from ID
    def get_tempandhumidity_fromID(self, ID):
        temp_and_humidity = self.sensor_contract.functions.getSensorDataByID(ID).call({"from":self.executor_address})

        return temp_and_humidity

    ## function to save swarm filehash to blockchain
    def set_filehash_blockchain(self, filehash):
        set_fn_txn_hash = self.sensor_contract.functions.setSensorData(filehash).transact({"from":self.executor_address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(set_fn_txn_hash)
        result = self.sensor_contract.events.setFileHashEvent().processReceipt(tx_receipt)
        return result[0]['args']

    ## function to get latest swarm filehash
    def get_filehash_latest(self):
        filehash = self.sensor_contract.functions.getSensorDataLatest().call({"from":self.executor_address})
        return filehash
    
    ## function to get swarm filehash using ID
    def get_filehash_id(self, id_req):
        filehash = self.sensor_contract.functions.getSensorDataByID(id_req).call({"from":self.executor_address})
        return filehash

    ## function to get current ID from blockchain
    def get_current_BCID(self):
        req_id = self.sensor_contract.functions.getCurrentID().call({"from":self.executor_address})
        return req_id

    ## Owner only Functions
    ## Register the IoT device
    def register_device(self, address_to_register):
        res_hash = self.sensor_contract.functions.registerDevice(address_to_register).transact({"from":self.executor_address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(res_hash)
        result = self.sensor_contract.events.deviceEvent().processReceipt(tx_receipt)
        return result[0]['args']

    ## De-Register the IoT device
    def deregister_device(self, address_to_deregister):
        res_hash = self.sensor_contract.functions.deregisterDevice(address_to_deregister).transact({"from":self.executor_address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(res_hash)
        result = self.sensor_contract.events.deviceEvent().processReceipt(tx_receipt)
        return result[0]['args']
    