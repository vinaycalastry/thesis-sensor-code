#!/usr/bin/python3

import os
import datetime
import time
import project_settings
import requests
import json
import zymkey
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

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

## Read the encrypted secret key
with open("temp.bin") as f:
    content = f.readlines()

## Store secret key for the duration of the session
secret_key = zymkey.client.unlock(base64.b64decode(content[0]))
secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")

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


while True:
    ## Get readings
    current_temperature, current_humidity = dht11_sensor_instance.get_dht_readings()

    ## Create a payload tot store in Swarm
    swarm_store = create_payload(current_temperature, current_humidity)

    ## Convert payload to bytes
    payload_str = bytes(swarm_store, "utf-8")

    ## Encrypt payload with AES
    cipher = AES.new(secret_key_b, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(payload_str, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode("utf-8")
    ct = base64.b64encode(ct_bytes).decode("utf-8")
    result = json.dumps({ "iv": iv, "ciphertext": ct})

    ## Send POST request to swarm to store the payload
    r = requests.post(project_settings.swarm_blockchain_url, data=result, headers={'Content-Type': 'text/plain'})

    ## Store the received filehash for swarm
    filehash = r.text

    ## Save the filehash in blockchain
    smart_contract_instance.set_filehash_blockchain(filehash)

    ## Printing Result to console
    print("Temp: ",current_temperature," and Humidity: ",current_humidity," set at: ", str(datetime.datetime.now()))

    ## Sleep for the required time
    time.sleep(time_recheck_reading)
