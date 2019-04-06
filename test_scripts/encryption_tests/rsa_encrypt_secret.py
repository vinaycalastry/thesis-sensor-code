#!/usr/bin/python3
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import random
from Cryptodome.Util.number import long_to_bytes
import base64
import hashlib
import hmac

# Size of hmac key
SIG_SIZE = hashlib.sha256().digest_size

# Generate random secret key
def get_random_bytes(amount):
    return long_to_bytes(random.getrandbits(amount * 8))

#Encrypt secret key with RSA public key
aes_key = get_random_bytes(AES.block_size) #lock it after first time
hmac_key = get_random_bytes(SIG_SIZE) #lock it after first time

print("Randome keys generated: AES, hmac")
print(aes_key)
print(hmac_key)

# Cipher and Key for producer
key_p = RSA.importKey(open('producer_public_key.pem').read())
cipher_p = PKCS1_OAEP.new(key_p)
producer_aes_cipher = cipher_p.encrypt(aes_key)
producer_hmac_cipher = cipher_p.encrypt(hmac_key)

# Cipher and Key for Consumer
key_c = RSA.importKey(open('consumer_public_key.pem').read())
cipher_c = PKCS1_OAEP.new(key_c)
consumer_aes_cipher = cipher_c.encrypt(aes_key)
consumer_hmac_cipher = cipher_c.encrypt(hmac_key)

#Send rsa cipher to producer file
encrypted_p_aes = open("rsa_ciphertext_producer.dat", mode='wb')
encrypted_p_aes.write(base64.b64encode(producer_aes_cipher))
encrypted_p_aes.close()

encrypted_p_hmac = open("hmac_ciphertext_producer.dat", mode='wb')
encrypted_p_hmac.write(base64.b64encode(producer_hmac_cipher))
encrypted_p_hmac.close()

#Send rsa cipher to consumer file
encrypted_c_aes = open("rsa_ciphertext_consumer.dat", mode='wb')
encrypted_c_aes.write(base64.b64encode(consumer_aes_cipher))
encrypted_c_aes.close()

encrypted_c_hmac = open("hmac_ciphertext_consumer.dat", mode='wb')
encrypted_c_hmac.write(base64.b64encode(consumer_hmac_cipher))
encrypted_c_hmac.close()