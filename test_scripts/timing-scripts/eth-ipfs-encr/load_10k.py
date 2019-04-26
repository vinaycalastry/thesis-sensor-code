#!/usr/bin/python3
import json
import datetime
import requests
import os
import sys
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import hmac
sys.path.append("../../..")
import ipfsapi
## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
import project_settings

# Use HMAC algorithm
HMAC_ALGO = hashlib.sha256

## blockchain url and addresses
smart_contract_address = project_settings.smart_contract_address
eth_blockchain_url = "http://192.168.0.20:8043"
abi_filename = os.path.abspath("../../../abi/contract_abi.json")
api = ipfsapi.connect('127.0.0.1', 5001)
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

#total_payload = total_payload[0:5000]

print("LOAD TEST DATA")
print("Start ID stored in the Ethereum Blockchain is: ", str(smart_contract_instance.get_current_BCID()))
secret_key_b = bytearray(b'\xdf\x9a|\x85\x03\xe6\xcd\xe3\r\xdbB~\x9f\xe4\xff\xe4')
secret_key_hmac_b = bytearray(b'\x14\xa0\xbd{\xd6O\xfd\xf8\xdc\x94\xa1\xf1\xf31\xd1\xc9\xa9\x84\x06\xb69q3\x85\xfa\x80\xee\x04<\x1b\x16k')
counter = 0
#START TEST
print("BEGIN COUNTING TIME")
print("RECORDS - TIME")
start = datetime.datetime.now()
for i in total_payload:

    payload_str = bytes(json.dumps(i), "utf-8")
    ## Encrypt payload with AES
    cipher = AES.new(secret_key_b, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(payload_str, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode("utf-8")
    ct = base64.b64encode(ct_bytes).decode("utf-8")

    iv_data = cipher.iv + ct_bytes
    sig = hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest()
    sig = base64.b64encode(sig).decode("utf-8")

    x = json.dumps({ "iv": iv, "ciphertext": ct, "signature": sig})
    r = api.add_str(x)
    #filehashes.append(r.text)
    counter += 1
    smart_contract_instance.set_filehash_blockchain_test(r)

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
