#/usr/bin/python3
import json
import datetime
import requests

total_payload = list()
filehashes = list()
with open('payload_1000.json', 'r') as f:
    total_payload = json.load(f)

start = datetime.datetime.now()
for i in total_payload:
    x = json.dumps(i)
    r = requests.post("http://localhost:8500/bzz:/",data=x , headers={'Content-Type': 'text/plain'})
    filehashes.append(r.text)

end = datetime.datetime.now()

with open('filehashes_1000', 'w') as f:
    f.write(filehashes)

print("Time taken for loading: "+ len(total_payload) + " records is : "+ (end-start).seconds+ " seconds.")