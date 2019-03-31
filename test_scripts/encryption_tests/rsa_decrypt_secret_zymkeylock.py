#!/usr/bin/python3
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import zymkey
import base64
import sys
import json

# pass the ciphertext file as argument to script 1: aes cipher, 2: hmac cipher
ciphertext_rsa = open(sys.argv[1]).read()
ciphertext_hmac = open(sys.argv[2]).read()

#Decrypt secret key with RSA private key
key_d = RSA.importKey(open('private_key.pem').read())
cipher_d = PKCS1_OAEP.new(key_d)
message_rsa = cipher_d.decrypt(base64.b64decode(ciphertext_rsa))
message_hmac = cipher_d.decrypt(base64.b64decode(ciphertext_hmac))

#Lock the aes secret to the zymkey
encrypted_f = open("zymkey_protected_secret_aes.dat", mode='wb')
locked_data = zymkey.client.lock(message_rsa)
encrypted_f.write(base64.b64encode(locked_data))
encrypted_f.close()

#Lock the hmac secret to the zymkey
encrypted_f = open("zymkey_protected_secret_hmac.dat", mode='wb')
locked_data = zymkey.client.lock(message_hmac)
encrypted_f.write(base64.b64encode(locked_data))
encrypted_f.close()

# AES key in locked form, unlock for test
content_aes = bytearray(open("zymkey_protected_secret_aes.dat", mode="rb").read())
print("Locked AES key: "+content_aes)
secret_key_aes = zymkey.client.unlock(base64.b64decode(content_aes))
print("AES key: "+secret_key_aes)

# hmac key in locked form, unlock for test
content_hmac = bytearray(open("zymkey_protected_secret_hmac.dat", mode="rb").read())
print("Locked HMAC key: "+content_hmac)
secret_key_hmac = zymkey.client.unlock(base64.b64decode(content_hmac))



#print(secret_key.decode("utf-8"))
#secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")