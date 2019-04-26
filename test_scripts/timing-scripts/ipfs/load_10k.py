#!/usr/bin/python3
import json
import datetime
import ipfsapi

total_payload = list()
filehashes = list()
filedir = "../data/"
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

time_taken_dict = {}
api = ipfsapi.connect('192.168.0.20', 5001)

print("BEGIN IPFS TEST")
#Load test file data to python object
with open(filedir + 'payload_10k.json', 'r') as f:
    total_payload = json.load(f)
print("LOAD TEST DATA")
total_payload = total_payload

counter = 0
#START TEST
print("BEGIN COUNTING TIME")
start = datetime.datetime.now()
for i in total_payload:
    x = json.dumps(i)
    r = api.add_str(x)
    filehashes.append(r)
    counter += 1
    
    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
        print(str(counter) + " - " + time_taken_dict[counter])
#END TEST
print("END COUNTING TIME")

print("WRITE FILE FOR READ TEST")
#SAVE FILEHASH for TESTING READ
with open('filehashes_10K', 'w') as f:
    f.write("\n".join(filehashes))


print("Filehashes saved for test")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)