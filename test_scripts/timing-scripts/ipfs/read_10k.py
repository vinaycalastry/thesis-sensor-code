#!/usr/bin/python3
import json
import datetime
import requests
import ipfsapi

total_payload = list()
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
time_taken_dict = {}

api = ipfsapi.connect('192.168.0.20', 5001)

print("BEGIN IPFS TEST")
#Store payload data from test file to python object
with open('filehashes_10K', 'r') as f:
    filehashes = f.readlines()

print("FILE HASHES LOADED")
#Convert string to list
filehashes = [x.strip() for x in filehashes]

print("BEGIN COUNTING TIME")
counter = 0
#START TEST
start = datetime.datetime.now()
for i in filehashes:
    res = api.get_json(i)
    total_payload.append(res)
    counter += 1

    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
print("END COUNTING TIME")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)