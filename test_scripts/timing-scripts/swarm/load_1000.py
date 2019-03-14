#/usr/bin/python3
import json
import datetime
import requests

total_payload = list()
filehashes = list()
with open('payload_1000.json', 'r') as f:
    total_payload = json.load(f)

start = datetime.datetime.now()
for i in total_payload:
    res = requests.get("http://localhost:8500/bzz:/"+i+"/")
    total_payload.append(res.text)

end = datetime.datetime.now()

with open('filehashes_1000', 'w') as f:
    f.write(filehashes)

print("SWARM: Time taken for reading: "+ len(total_payload) + " records is : "+ (end-start).seconds+ " seconds.")