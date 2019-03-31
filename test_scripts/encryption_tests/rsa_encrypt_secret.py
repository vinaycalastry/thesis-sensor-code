#!/usr/bin/python3
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import random
from Cryptodome.Util.number import long_to_bytes
import base64
import hashlib
import hmac
import json

# Size of hmac key
SIG_SIZE = hashlib.sha256().digest_size

# Generate random secret key
def get_random_bytes(amount):
    return long_to_bytes(random.getrandbits(amount * 8))

#Encrypt secret key with RSA public key
aes_key = get_random_bytes(AES.block_size)
hmac_key = get_random_bytes(SIG_SIZE)

print("Randome keys generated: AES, hmac")
print(aes_key)
print(hmac_key)

key = RSA.importKey(open('public_key.pem').read())
cipher = PKCS1_OAEP.new(key)
aes_cipher = cipher.encrypt(aes_key)
hmac_cipher = cipher.encrypt(hmac_key)

#Send cipher to file
encrypted_f = open("rsa_ciphertext.dat", mode='wb')
encrypted_f.write(base64.b64encode(json.dumps({"aes_cipher": aes_cipher, "hmac_cipher": hmac_cipher})))
encrypted_f.close()