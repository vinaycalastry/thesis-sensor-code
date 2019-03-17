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

#Decrypt secret key with RSA private key
key_d = RSA.importKey(open('private_key.pem').read())
cipher_d = PKCS1_OAEP.new(key_d)
message = cipher_d.decrypt(ciphertext)

#Lock the secret to the zymkey
encrypted_f = open("zymkey_protected_secret.dat", mode='wb')
locked_data = zymkey.client.lock(message)
encrypted_f.write(base64.b64encode(locked_data))
encrypted_f.close()

content = bytearray(open("zymkey_protected_secret.dat", mode="rb").read())

print(content)
secret_key = zymkey.client.unlock(base64.b64decode(content))

print(secret_key.decode("utf-8"))
secret_key_b = bytes(secret_key.decode("utf-8"), "utf-8")
