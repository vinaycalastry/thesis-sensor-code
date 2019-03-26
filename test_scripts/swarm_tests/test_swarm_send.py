#!/usr/bin/python3

import requests
import json

payload = {'temp': '23C', 'humidity': 85}
x = json.dumps(payload)
r = requests.post("http://localhost:8500/bzz:/",data=x , fi;e)
filehash = r.text
print("Filehash is: ",filehash)
