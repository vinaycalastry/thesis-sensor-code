#!/usr/bin/python3

import requests
requests.packages.urllib3.disable_warnings()
import json

payload = {'temp': '23C', 'humidity': 85}
x = json.dumps(payload)
r = requests.post("https://192.168.0.16/",data=x , headers={'Content-Type': 'text/plain'},verify=False)

filehash = r.text

res = requests.get("https://192.168.0.16/"+filehash+"/", verify=False)

print(json.loads(res.text))