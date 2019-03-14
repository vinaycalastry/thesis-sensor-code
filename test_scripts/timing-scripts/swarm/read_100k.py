#!/usr/bin/python3
import json
import datetime
import requests

total_payload = list()

#Store payload data from test file to python object
with open('filehashes_100K', 'r') as f:
    filehashes = f.readlines()

#Convert string to list
filehashes = [x.strip() for x in filehashes]

#START TEST
start = datetime.datetime.now()
for i in filehashes:
    res = requests.get("http://localhost:8500/bzz:/"+i+"/")
    total_payload.append(res.text)

#END TEST
end = datetime.datetime.now()

#Display result
print("SWARM: Time taken for loading: "+ str(len(total_payload)) + " records is : "+ str((end-start).seconds) + " seconds.")
