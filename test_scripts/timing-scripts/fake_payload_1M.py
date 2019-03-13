
import datetime
import json
import random

generate_size = [1000, 100000, 1000000]

## Create payload to store in swarm
def create_payload(temperature, humidity):
    """
        Data to store as payload in swarm
        1. Temperature
        2. Humidity
        3. Temperature Units (Celsius)
        4. Humidity Units (%)
        5. Timestamp
        6. Device type
        7. Device ID
        8. Device IP
        9. Sensor Type
    """
    
    ## Get current time
    current_time = str(datetime.datetime.now())

    payload = {
        "Temperature": temperature,
        "Humidity": humidity,
        "TemperatureUnits": "Celsius",
        "HumidityUnits": "%",
        "Timestamp": current_time,
        "DeviceType": "Raspberry Pi 3B+",
        "DeviceID": "IoTProducer1",
        "DeviceIP": "192.168.0.16",
        "SensorType": "DHT11"
    }
    return payload


total_payload_1000 = []
total_payload_100k = []
total_payload_1M = []

#file_1000
for i in range(generate_size[0]):
    temp = random.randint(8,49)
    humi = random.randint(20,81)
    total_payload_1000.append(create_payload(temp, humi))

with open('payload_1000.json', 'w') as f:
    json.dump(total_payload_1000, f)

#file_100k
for i in range(generate_size[1]):
    temp = random.randint(8,49)
    humi = random.randint(20,81)
    total_payload_100k.append(create_payload(temp, humi))

with open('payload_100k.json', 'w') as f:
    json.dump(total_payload_100k, f)

#file_1M
for i in range(generate_size[2]):
    temp = random.randint(8,49)
    humi = random.randint(20,81)
    total_payload_1M.append(create_payload(temp, humi))

with open('payload_1M.json', 'w') as f:
    json.dump(total_payload_1M, f)