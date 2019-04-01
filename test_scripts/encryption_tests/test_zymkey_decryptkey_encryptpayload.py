### Install pycryptodomex for this to work
### Credits to: https://gist.github.com/dirkmoors/9812522

import zymkey
import base64
import json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import requests
import json
import hashlib
import hmac

# Use HMAC algorithm
HMAC_ALGO = hashlib.sha256

# Compare MAC signatures
def compare_mac(mac, mac_verif):
    if len(mac) != len(mac_verif):
        print ("invalid MAC size")
        return False

    result = 0
    for x, y in zip(mac, mac_verif):
        result |= x ^ y
    return result == 0

# open aes key data
content = bytearray(open("zymkey_protected_secret_aes.dat", mode="rb").read())
secret_key = zymkey.client.unlock(base64.b64decode(content))
secret_key_b = bytearray(secret_key)

# open hmac key data
content_hmac = bytearray(open("zymkey_protected_secret_hmac.dat", mode="rb").read())
secret_key_hmac = zymkey.client.unlock(base64.b64decode(content_hmac))
secret_key_hmac_b = bytearray(secret_key_hmac)

# Generate payload and convert to serializable json
payload = {"temp": "23C", "humidity": "80%"}
payload_str = bytes(json.dumps(payload), "utf-8")

## Encryption and Sign

# Generate cipher
cipher = AES.new(secret_key_b, AES.MODE_CBC)

# Encrypt data using cipher
ct_bytes = cipher.encrypt(pad(payload_str, AES.block_size))

# Save Initialization vector and Cipher content
iv = base64.b64encode(cipher.iv).decode("utf-8")
ct = base64.b64encode(ct_bytes).decode("utf-8")

# Generate Signature
iv_data = cipher.iv + ct_bytes
sig = hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest()
sig = base64.b64encode(sig).decode("utf-8")

# Save Cipher and Signature to serializable json
result = json.dumps({ "iv": iv, "ciphertext": ct, "signature": sig})

print("------------------")
print("CIPHER TEXT: ")
print(result)
print("-------------------")

## Send to swarm
x = result
r = requests.post("http://127.0.0.1:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})

filehash = r.text

## Get the contents from swarm
res = requests.get("http://127.0.0.1:8500/bzz:/"+filehash+"/")
to_decode = res.text

## Verification and Decryption 

try:
    b64 = json.loads(to_decode)
    iv_d = base64.b64decode(b64["iv"])
    ct_d = base64.b64decode(b64["ciphertext"])
    sig_d = base64.b64decode(b64["signature"])
    cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)
    
    iv_data = iv_d+ct_d

    if not compare_mac(hmac.new(secret_key_hmac_b, iv_data, HMAC_ALGO).digest(), sig_d):
        raise ValueError
    else:
        pt = unpad(cipher_d.decrypt(ct_d), AES.block_size)
        result_d = pt.decode()
        print("--------------")
        print("PLAINTEXT: ")
        print("The message is authentic: ", result)

except ValueError:
    print("Key is incorrect or msg is corrupted")