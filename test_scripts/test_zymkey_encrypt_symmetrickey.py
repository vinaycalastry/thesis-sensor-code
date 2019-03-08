import base64
import zymkey
import logging
import json


## Generate a key
key = "8CDE5C6788226D6C12643F1588E28123"

encrypted_f = open("temp.bin", mode='wb')

locked_data = zymkey.client.lock(bytearray(key))


logging.info("Locked data")

print(locked_data)

encrypted_f.write(base64.b64encode(locked_data)+'\n')

