import firebase_admin
from firebase_admin import credentials, db
import csv

# Initialize Firebase
cred = credentials.Certificate("task5-805bf-firebase-adminsdk-fbsvc-bbe15c788a.json")  # Replace with your Firebase credentials JSON file
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://task5-805bf-default-rtdb.firebaseio.com/"  # Replace with your Firebase database URL
})

# Reference Firebase database
ref = db.reference("gyro_data")  # Ensure this matches the Firebase node where data is stored
data = ref.get()

if data:
    # Open a CSV file for writing
    with open("gyro_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "x", "y", "z"])  # Column headers
        
        # Loop through Firebase data and write to CSV
        for key, value in data.items():
            writer.writerow([value["timestamp"], value["x"], value["y"], value["z"]])

    print("CSV file saved successfully as 'gyro_data.csv'!")
else:
    print("No data found in Firebase.")
