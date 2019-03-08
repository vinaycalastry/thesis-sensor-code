### Install pycryptodomex for this to work
import zymkey
import base64
import json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import requests
import json

with open("temp.bin") as f:
    content = f.readlines()

secret_key = zymkey.client.unlock(base64.b64decode(content[0]))

#secret_key_str = secret_key.decode()
secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")

payload = {"temp": "23C", "humidity": "80%"}

payload_str = bytes(json.dumps(payload), "utf-8")

## Encryption
cipher = AES.new(secret_key_b, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(payload_str, AES.block_size))
iv = base64.b64encode(cipher.iv).decode("utf-8")
ct = base64.b64encode(ct_bytes).decode("utf-8")
result = json.dumps({ "iv": iv, "ciphertext": ct})


print("------------------")
print("CIPHER TEXT: ")
print(result)
print("-------------------")

## Send to swarm
x = result
r = requests.post("http://localhost:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})

filehash = r.text

## Get the contents from swarm
res = requests.get("http://localhost:8500/bzz:/"+filehash+"/")
to_decode = res.text

## Decryption

try:
    b64 = json.loads(to_decode)
    iv_d = base64.b64decode(b64["iv"])
    ct_d = base64.b64decode(b64["ciphertext"])
    cipher_d = AES.new(secret_key_b, AES.MODE_CBC, iv_d)
    pt = unpad(cipher_d.decrypt(ct_d), AES.block_size)
    print("--------------")
    print("PLAINTEXT: ")
    print("The message is authentic: ", pt.decode())

except ValueError:
    print("Key is incorrect or msg is corrupted")