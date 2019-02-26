#!/usr/bin/python3

import requests
import json
import sys


filehash = sys.argv[1]
print("Filehash is: ", filehash)

res = requests.get("http://localhost:8500/bzz:/"+filehash+"/")

print(json.loads(res.text))