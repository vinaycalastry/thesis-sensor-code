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
from interfacer_modules.sensors import I2C_LCD_driver


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

## LCD sensor init
lcd_sensor_instance = I2C_LCD_driver.lcd()

## Helper function for degree conversion from fahrenheit to celsius
def fahrenheit_to_celsius(temperature):
    return round((temperature * 9/5) + 32)

## Helper function for degree conversion from celsius to fahrenheit
def celsius_to_fahrenheit(temperature):
    return round(temperature * 1.8 + 32)

## Read the encrypted secret key
with open("temp.bin") as f:
    content = f.readlines()

## Store secret key for the duration of the session
secret_key = zymkey.client.unlock(base64.b64decode(content[0]))
secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")

while True:
    try:    
        ## Get filehash from swarm
        filehash_swarm = smart_contract_instance.get_filehash_latest()

        ## Get encrypted payload stored in filehash from swarm
        res = requests.get(project_settings.swarm_blockchain_url+filehash_swarm+"/")
        payload_res = res.text

        ## Decrypt the payload
        b64 = json.loads(payload_res)
        iv_d = base64.b64decode(b64["iv"])
        ct_d = base64.b64decode(b64["ciphertext"])
        cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)
        decrypted_payload = unpad(cipher_d.decrypt(ct_d), AES.block_size)

        ## Convert bytes array to dictionary
        payload_final = json.loads(decrypted_payload.decode())

        ## Get the temperature, hulidity and timestamp stored
        temp_in_f = celsius_to_fahrenheit(payload_final["Temperature"])
        humidity = payload_final["Humidity"]
        time_captured = payload_final["Timestamp"]

        ## Display results in the LCD
        lcd_sensor_instance.lcd_clear() 
        lcd_sensor_instance.lcd_display_string("Temp: "+str(temp_in_f)+"F", project_settings.TEMP_DISPLAY, project_settings.OFFSET)
        lcd_sensor_instance.lcd_display_string("Humidity: "+str(humidity)+"%", project_settings.HUMIDITY_DISPLAY, project_settings.OFFSET)

        ## Sleep and restart
        time.sleep(time_recheck_reading)

    except KeyboardInterrupt:
        lcd_sensor_instance.lcd_clear()
        lcd_sensor_instance.lcd_display_string("Closed")

