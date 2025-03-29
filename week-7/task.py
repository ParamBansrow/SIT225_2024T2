import serial
import csv
import time


port = "COM5"  
baud_rate = 9600  

csv_file = "sensor_data.csv"  
columns = ["Time ", "Temperature ", "Humidity "]  

# Initialize serial communication
try:
    ser = serial.Serial(port, baud_rate, timeout=1)
    print(f"Connected to {port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Error: Could not open port {port}. {e}")
    exit()

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)  

    print("Collecting data. Press Ctrl+C to stop.")

    try:
        while True:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                print(f"Data received: {line}")
                # Split the data into components
                try:
                    data = line.split(",")  
                    if len(data) == 3:  
                        writer.writerow(data)  
                except ValueError as ve:
                    print(f"Error processing line: {line}. {ve}")

    except KeyboardInterrupt:
        print("\nData collection stopped.")

# Close the serial port
ser.close()
print(f"Data saved to {csv_file}.")