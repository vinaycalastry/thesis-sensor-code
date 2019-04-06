#!/usr/bin/python3

## blockchain url and addresses
smart_contract_address = "0x600D3053C6c8C164fF0B8385D3DC1cD19Db7c7C8"
eth_blockchain_url = "http://localhost:8042"
abi_filename = "abi/contract_abi.json"

## eth-swarm data
swarm_blockchain_url = "http://localhost:8500/bzz:/"
device_type = "Raspberry PI 3B+"
producer_device_id = "IoTProducer1"
consumer_device_id = "IoTConsumer1"

## IOT sensor values
sensor_type = "DHT11"
dht_version = 11
time_recheck_reading = 60
dht_GPIO = 22

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
