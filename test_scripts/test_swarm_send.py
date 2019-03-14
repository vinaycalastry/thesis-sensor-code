#!/usr/bin/python3

import requests
import json

payload = {'temp': '23C', 'humidity': 85}
x = json.dumps(payload)
r = requests.post("http://localhost:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})
filehash = r.text
print("Filehash is: ",filehash)
