#!/usr/bin/python3
import json
import datetime
import requests
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import hmac
import ipfsapi


# Use HMAC algorithm
HMAC_ALGO = hashlib.sha256

total_payload = list()
filehashes = list()
filedir = "../data/"
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
time_taken_dict = {}

print("BEGIN SWARM TEST")
#Load test file data to python object
with open(filedir + 'payload_10k.json', 'r') as f:
    total_payload = json.load(f)
print("LOAD TEST DATA")

total_payload = total_payload
secret_key_b = bytearray(b'\xdf\x9a|\x85\x03\xe6\xcd\xe3\r\xdbB~\x9f\xe4\xff\xe4')
secret_key_hmac_b = bytearray(b'\x14\xa0\xbd{\xd6O\xfd\xf8\xdc\x94\xa1\xf1\xf31\xd1\xc9\xa9\x84\x06\xb69q3\x85\xfa\x80\xee\x04<\x1b\x16k')
api = ipfsapi.connect('192.168.0.20', 5001)
counter = 0
#START TEST
print("BEGIN COUNTING TIME")
print("RECORDS - TIME")
start = datetime.datetime.now()
for i in total_payload:
    payload_str = bytes(json.dumps(i), "utf-8")
    ## Encrypt payload with AES
    cipher = AES.new(secret_key_b, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(payload_str, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode("utf-8")
    ct = base64.b64encode(ct_bytes).decode("utf-8")

    iv_data = cipher.iv + ct_bytes
    sig = hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest()
    sig = base64.b64encode(sig).decode("utf-8")

    x = json.dumps({ "iv": iv, "ciphertext": ct, "signature": sig})
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