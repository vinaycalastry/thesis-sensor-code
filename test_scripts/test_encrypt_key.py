import base64
import zymkey
import logging
import json

payload = { 'temp' : "23C", 'humidity' : "100%"}
data_to_encrypt = json.dumps(payload)

print(type(data_to_encrypt))

#new_data = bytearray(data_to_encrypt)
#print(new_data)

encrypted_f = open("temp.bin", mode='wb')

locked_data = zymkey.client.lock(bytearray('1231241rwqsfas12'))



logging.info("Locked data")
print(locked_data)

encrypted_f.write(base64.b64encode(locked_data)+'\n')

