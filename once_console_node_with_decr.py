#!/usr/bin/python3

import os
import datetime
import time
import requests
requests.packages.urllib3.disable_warnings()
import json
#import zymkey
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
print("Smart contract is loaded")
## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

## LCD sensor init
lcd_sensor_instance = I2C_LCD_driver.lcd()
print("LCD driver is loaded")
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
#content = bytearray(open("zymkey_protected_secret_aes.dat", mode="rb").read())
#secret_key = zymkey.client.unlock(base64.b64decode(content))
secret_key_b = bytearray(b'\xdf\x9a|\x85\x03\xe6\xcd\xe3\r\xdbB~\x9f\xe4\xff\xe4')
print("Secret AES key unlocked")

## Open hmac key data
#content_hmac = bytearray(open("zymkey_protected_secret_hmac.dat", mode="rb").read())
#secret_key_hmac = zymkey.client.unlock(base64.b64decode(content_hmac))
secret_key_hmac_b = bytearray(b'\x14\xa0\xbd{\xd6O\xfd\xf8\xdc\x94\xa1\xf1\xf31\xd1\xc9\xa9\x84\x06\xb69q3\x85\xfa\x80\xee\x04<\x1b\x16k')
print("Secret HMAC key unlocked")

print()
print("Sequence of steps to retrieve data:")
while True:
    try:
        ## Get filehash from swarm
        filehash_swarm = smart_contract_instance.get_filehash_latest()
        print("1. Get Latest filehash from Ethereum Blockchain")
        print("Retrieved filehash is: ")
        print(filehash_swarm)

        ## Get encrypted payload stored in filehash from swarm
        res = requests.get(project_settings.swarm_blockchain_url+filehash_swarm+"/", verify=False)
        payload_res = res.text
        print()
        print("2. Retrieve Encrypted Payload from Swarm")
        print(payload_res)

        ## Decrypt the payload and retrieve iv, signature and ciphertext
        b64 = json.loads(payload_res)
        iv_d = base64.b64decode(b64["iv"])
        sig_d = base64.b64decode(b64["signature"])
        ct_d = base64.b64decode(b64["ciphertext"])
        cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)

        ## Generate iv data to recreate and check signature
        iv_data = iv_d+ct_d

        print()
        print("3. Retrieved Signature is:")
        print(sig_d)

        ## Verify signature using MAC
        if not compare_mac(hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest(), sig_d):
            raise ValueError
        else:
            pt = unpad(cipher_d.decrypt(ct_d), AES.block_size)
            result_d = pt.decode()

        ## Convert bytes array to dictionary
        payload_final = json.loads(result_d)
        print()
        print("4. Retrieved Payload from Swarm and decrypt it")
        print(payload_final)

        ## Get the temperature, hulidity and timestamp stored
        temp_in_f = celsius_to_fahrenheit(payload_final["Temperature"])
        humidity = payload_final["Humidity"]
        time_captured = payload_final["Timestamp"]

        print("5. Setting LCD values")
        ## Display results in the LCD
        lcd_sensor_instance.lcd_clear()
        lcd_sensor_instance.lcd_display_string("Temp: "+str(temp_in_f)+"F", project_settings.TEMP_DISPLAY, project_settings.OFFSET)
        lcd_sensor_instance.lcd_display_string("Humidity: "+str(humidity)+"%", project_settings.HUMIDITY_DISPLAY, project_settings.OFFSET)

        ## Sleep and restart
        #time.sleep(time_recheck_reading)
        break

    except KeyboardInterrupt:
        lcd_sensor_instance.lcd_clear()
        lcd_sensor_instance.lcd_display_string("Closed")
        break

    except ValueError:
        print("Key is incorrect or msg is corrupted")
        break