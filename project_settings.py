#!/usr/bin/python3

## blockchain url and addresses
smart_contract_address = "0xab0e8bda0aa2b653e7f20f96261db5ef45afa6b7"
eth_blockchain_url = "http://localhost:8042"
abi_filename = "abi/contract_abi.json"

## IOT sensor values
dht_version = 11
time_recheck_reading = 60
dht_GPIO = 4

## LCD settings
I2CBUS = 1  # 0 for rpi1, 1 for later
I2CADDRESS = 0x27 # I2C address, get it by running i2cdetect -y 1
OFFSET = 0
TEMP_DISPLAY = 1
HUMIDITY_DISPLAY = 2

## LED values
RED = 4
GREEN = 3
BLUE = 2
times_to_blink = 5
time_recheck_reading = 60