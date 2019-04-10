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
benchmark_steps = [10, 100, 250, 500, 750, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
time_taken_dict = {}

secret_key_b = bytearray(b'\xdf\x9a|\x85\x03\xe6\xcd\xe3\r\xdbB~\x9f\xe4\xff\xe4')
secret_key_hmac_b = bytearray(b'\x14\xa0\xbd{\xd6O\xfd\xf8\xdc\x94\xa1\xf1\xf31\xd1\xc9\xa9\x84\x06\xb69q3\x85\xfa\x80\xee\x04<\x1b\x16k')

print("BEGIN SWARM TEST")
#Store payload data from test file to python object
with open('filehashes_10K', 'r') as f:
    filehashes = f.readlines()

print("FILE HASHES LOADED")
#Convert string to list
filehashes = [x.strip() for x in filehashes]

# Compare MAC signatures
def compare_mac(mac, mac_verif):
    if len(mac) != len(mac_verif):
        print ("invalid MAC size")
        return False

    result = 0
    for x, y in zip(mac, mac_verif):
        result |= x ^ y
    return result == 0
api = ipfsapi.connect('192.168.0.15', 5001)
print("BEGIN COUNTING TIME")
counter = 0
#START TEST
start = datetime.datetime.now()
for i in filehashes:
    res = api.get_json(i)
    b64 = json.loads(res)
    iv_d = base64.b64decode(b64["iv"])
    sig_d = base64.b64decode(b64["signature"])
    ct_d = base64.b64decode(b64["ciphertext"])
    cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)
    iv_data = iv_d+ct_d

    if not compare_mac(hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest(), sig_d):
        raise ValueError
    else:
        pt = unpad(cipher_d.decrypt(ct_d), AES.block_size)
        result_d = pt.decode()
        total_payload.append(result_d)
    counter += 1

    if counter in benchmark_steps:
        end = datetime.datetime.now()
        time_taken_dict[counter] = str((end-start).seconds)
        print(str(counter) + " - " + time_taken_dict[counter])
print("END COUNTING TIME")

#Dictionary to save times taken for loading
print("TIMES TAKEN")
print(time_taken_dict)