#!/usr/bin/python3
import json
import datetime
import requests

total_payload = list()
filehashes = list()
with open('filehashes_1000', 'r') as f:
    filehashes = f.read()

start = datetime.datetime.now()
for i in total_payload:
    res = requests.get("http://localhost:8500/bzz:/"+i+"/")
    total_payload.append(res.text)

end = datetime.datetime.now()

print("SWARM: Time taken for loading: "+ len(filehashes) + " records is : "+ (end-start).seconds+ " seconds.")