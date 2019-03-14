#!/usr/bin/python3
import json
import datetime
import requests

total_payload = list()

with open('filehashes_1000', 'r') as f:
    filehashes = f.readlines()

filehashes = [x.strip() for x in filehashes]

start = datetime.datetime.now()
for i in filehashes:
    res = requests.get("http://localhost:8500/bzz:/"+i+"/")
    total_payload.append(res.text)

end = datetime.datetime.now()

print("SWARM: Time taken for loading: "+ str(len(total_payload)) + " records is : "+ str((end-start).seconds) + " seconds.")
