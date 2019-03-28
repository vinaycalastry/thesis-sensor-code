#!/usr/bin/python3
import json
import datetime
import requests
import ipfsapi

total_payload = list()
benchmark_steps = [10, 100, 1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
time_taken_dict = {}

api = ipfsapi.connect('127.0.0.1', 5001)

print("BEGIN IPFS TEST")
#Store payload data from test file to python object
with open('filehashes_100K', 'r') as f:
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