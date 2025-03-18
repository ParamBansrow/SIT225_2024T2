import paho.mqtt.client as mqtt
import pymongo
import json

# MongoDB Setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = mongo_client["GyroscopeDB"]
collection = db["GyroDB"]

# MQTT Configuration
MQTT_BROKER = "e42ea22cdfca44c9a56ff4d6bd9b1b13.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "gyro/data"
MQTT_USER = "hivemq.webclient.1742118867901"
MQTT_PASSWORD = "9832IYJKZpabAncd,.?&"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Connection failed with code:", rc)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received:", data)

    # Store data in MongoDB
    collection.insert_one(data)
    print("Data inserted into MongoDB!")

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set()  # Required for secure connection
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
