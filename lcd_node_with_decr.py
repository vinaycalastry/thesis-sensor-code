#!/usr/bin/python3

import os
import datetime
import time
import requests
import json
import zymkey
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import hmac

# Use HMAC algorithm
HMAC_ALGO = hashlib.sha256

## Custom modules
from interfacer_modules.blockchain.smartcontract import SmartContractCaller
from interfacer_modules.sensors import I2C_LCD_driver
import project_settings

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

## Helper functions
# Compare MAC signatures
def compare_mac(mac, mac_verif):
    if len(mac) != len(mac_verif):
        print ("invalid MAC size")
        return False

    result = 0
    for x, y in zip(mac, mac_verif):
        result |= x ^ y
    return result == 0

## Helper function for degree conversion from fahrenheit to celsius
def fahrenheit_to_celsius(temperature):
    return round((temperature * 9/5) + 32)

## Helper function for degree conversion from celsius to fahrenheit
def celsius_to_fahrenheit(temperature):
    return round(temperature * 1.8 + 32)


## Open aes key data
content = bytearray(open("zymkey_protected_secret_aes.dat", mode="rb").read())
secret_key = zymkey.client.unlock(base64.b64decode(content))
secret_key_b = bytearray(secret_key)

## Open hmac key data
content_hmac = bytearray(open("zymkey_protected_secret_hmac.dat", mode="rb").read())
secret_key_hmac = zymkey.client.unlock(base64.b64decode(content_hmac))
secret_key_hmac_b = bytearray(secret_key_hmac)

while True:
    try:    
        ## Get filehash from swarm
        filehash_swarm = smart_contract_instance.get_filehash_latest()

        ## Get encrypted payload stored in filehash from swarm
        res = requests.get(project_settings.swarm_blockchain_url+filehash_swarm+"/")
        payload_res = res.text

        ## Decrypt the payload and retrieve iv, signature and ciphertext
        b64 = json.loads(payload_res)
        iv_d = base64.b64decode(b64["iv"])
        sig_d = base64.b64decode(b64["signature"])
        ct_d = base64.b64decode(b64["ciphertext"])
        cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)

        ## Generate iv data to recreate and check signature
        iv_data = iv_d+ct_d

        ## Verify signature using MAC
        if not compare_mac(hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest(), sig_d):
            raise ValueError
        else:
            pt = unpad(cipher_d.decrypt(ct_d), AES.block_size)
            result_d = pt.decode()
            
        ## Convert bytes array to dictionary
        payload_final = json.loads(result_d)

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
        break

    except ValueError:
        print("Key is incorrect or msg is corrupted")
        break

