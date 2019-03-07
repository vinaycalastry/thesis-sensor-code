import zymkey
import base64

with open("temp.bin") as f:
    content = f.readlines()

payload = zymkey.client.unlock(base64.b64decode(content[0]))

print(type(payload))
print(payload.decode())
