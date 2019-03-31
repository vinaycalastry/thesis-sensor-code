#!/usr/bin/python3
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import zymkey
import base64
import sys
import json

# pass the ciphertext file as argument to script
ciphertext = open(sys.argv[1]).read()

#Decrypt secret key with RSA private key
key_d = RSA.importKey(open('private_key.pem').read())
cipher_d = PKCS1_OAEP.new(key_d)
message = cipher_d.decrypt(base64.b64decode(ciphertext))

#Lock the secret to the zymkey
encrypted_f = open("zymkey_protected_secret.dat", mode='wb')
locked_data = zymkey.client.lock(message)
encrypted_f.write(base64.b64encode(locked_data))
encrypted_f.close()

content = bytearray(open("zymkey_protected_secret.dat", mode="rb").read())

print(content)
secret_keys = zymkey.client.unlock(base64.b64decode(content))

print(json.loads(secret_keys))

#print(secret_key.decode("utf-8"))
#secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")