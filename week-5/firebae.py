import serial
import json
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("task5-805bf-firebase-adminsdk-fbsvc-bbe15c788a.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://task5-805bf-default-rtdb.firebaseio.com/"})

# Setup Serial Communication
ser = serial.Serial("COM7", 115200)  # Change COMx to your port, e.g., /dev/ttyUSB0 for Linux/Mac

while True:
    try:
        data = ser.readline().decode("utf-8").strip()
        if data:
            timestamp, x, y, z = data.split(",")
            entry = {
                "timestamp": int(timestamp),
                "x": float(x),
                "y": float(y),
                "z": float(z)
            }
            ref = db.reference("gyro_data").push()
            ref.set(entry)
            print("Uploaded:", entry)
    except Exception as e:
        print("Error:", e)
