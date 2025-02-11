import serial
import time
import random

# Ensure correct port based on your setup
arduino_port = "COM7"
baud_rate = 9600

try:
    with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
        print("Connected to Arduino!")

        while True:
            # Step 1: Generate and send a random number
            number_to_send = random.randint(1, 5)
            ser.write(f"{number_to_send}\n".encode())
            print(f"[{time.strftime('%H:%M:%S')}] Sent: {number_to_send}")

            # Step 3: Receive a number back from Arduino
            arduino_response = ser.readline().decode().strip()
            if arduino_response.isdigit():
                wait_time = int(arduino_response)
                print(f"[{time.strftime('%H:%M:%S')}] Received: {wait_time}")

                # Step 4: Sleep for the given number of seconds
                print(f"[{time.strftime('%H:%M:%S')}] Sleeping for {wait_time} seconds...")
                time.sleep(wait_time)
                print(f"[{time.strftime('%H:%M:%S')}] Done sleeping.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] No valid response from Arduino.")

except serial.SerialException:
    print("Could not connect to Arduino. Check the port configuration.")
