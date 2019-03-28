#!/usr/bin/python3
import json
import datetime
import ipfsapi

total_payload = list()
filehashes = list()
filedir = "/home/pi/vinay/test-payload/"
benchmark_steps = [10, 100, 1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
time_taken_dict = {}
api = ipfsapi.connect('127.0.0.1', 5001)

print("BEGIN IPFS TEST")
#Load test file data to python object
with open(filedir + 'payload_100k.json', 'r') as f:
    total_payload = json.load(f)
print("LOAD TEST DATA")

counter = 0
#START TEST
print("BEGIN COUNTING TIME")
start = datetime.datetime.now()
for i in total_payload:
    x = json.dumps(i)
    r = api.add_json(x)
    filehashes.append(r)
    counter += 1

    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
#END TEST
print("END COUNTING TIME")

print("WRITE FILE FOR READ TEST")
#SAVE FILEHASH for TESTING READ
with open('filehashes_100K', 'w') as f:
    f.write("\n".join(filehashes))


print("Filehashes saved for test")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)