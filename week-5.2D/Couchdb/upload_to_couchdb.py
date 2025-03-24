import paho.mqtt.client as mqtt
import couchdb
import json

# CouchDB Connection
couch = couchdb.Server("http://Param:aus2112@127.0.0.1:5984/")
db_name = "gyro_data"
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# MQTT Credentials
BROKER = "e42ea22cdfca44c9a56ff4d6bd9b1b13.s1.eu.hivemq.cloud"
PORT = 8883  # SSL Port
USERNAME = "hivemq.webclient.1742118867901"
PASSWORD = "9832IYJKZpabAncd,.?&"
TOPIC = "gyro/data"

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to HiveMQ")
        client.subscribe(TOPIC)
    else:
        print(f" Failed to connect, return code {rc}")

# Callback for receiving messages
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        print(f" Received: {payload}")
        db.save(payload)  # Save to CouchDB
    except Exception as e:
        print(f" Error: {e}")

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

# Enable SSL/TLS
client.tls_set()  # Automatically sets SSL for secure connection

client.on_connect = on_connect
client.on_message = on_message

print(" Connecting to MQTT...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
