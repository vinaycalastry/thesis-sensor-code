#!/usr/bin/python3
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import zymkey
import base64

#Encrypt secret key with RSA public key
secret = b"8CDE5C6788226D6C12643F1588E28123"
key = RSA.importKey(open('public_key.pem').read())
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(secret)

#Send cipher to file
encrypted_f = open("rsa_ciphertext.dat", mode='wb')
encrypted_f.write(base64.b64encode(ciphertext))
encrypted_f.close()