#!/usr/bin/python3

import ipfsapi
import requests
import json

payload = {'temp': '23C', 'humidity': 85}
x = json.dumps(payload)

api = ipfsapi.connect('127.0.0.1', 5001)
print(api.add_json(x))