import serial
import time
import csv


ser = serial.Serial('COM7', 9600, timeout=1)  
time.sleep(2)  


filename = "dht22_data.csv"
with open(filename, 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Timestamp", "Temperature (C)", "Humidity (%)"]) 
    print("\nData collection started!") 
    while True:
        try:
            
            data = ser.readline().decode('utf-8').strip()

            if data and "Error" not in data:
                
                parts = data.split(",")
                timestamp = time.strftime("%Y%m%d%H%M%S")  
                temperature = parts[1]
                humidity = parts[2]

                
                csv_writer.writerow([timestamp, temperature, humidity])
                print(f"Logged: {timestamp}, {temperature}C, {humidity}%")

        except KeyboardInterrupt:
            print("\nData collection stopped.")
            break  


ser.close()
