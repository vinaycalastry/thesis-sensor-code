#!/usr/bin/python3
import json
import datetime
import requests

total_payload = list()
filehashes = list()
filedir = "/home/pi/vinay/test-payload/"

#Load test file data to python object
with open(filedir + 'payload_1M.json', 'r') as f:
    total_payload = json.load(f)

#START TEST
start = datetime.datetime.now()
for i in total_payload:
    x = json.dumps(i)
    r = requests.post("http://localhost:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})
    filehashes.append(r.text)
#END TEST
end = datetime.datetime.now()

#SAVE FILEHASH for TESTING READ
with open('filehashes_1M', 'w') as f:
    f.write("\n".join(filehashes))

#Calculate total time taken
total_time = str((end-start).seconds)

print("SWARM: Time taken for reading: "+ str(len(total_payload)) + " records is : "+total_time+ " seconds.")
