#include <Arduino_LSM6DS3.h>

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
    Serial.println("Gyroscope initialized");
}

void loop() {
    float x, y, z;
    
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);
        Serial.print(millis()); // Timestamp
        Serial.print(",");
        Serial.print(x);
        Serial.print(",");
        Serial.print(y);
        Serial.print(",");
        Serial.println(z);
    }

    delay(100); // Adjust this based on required sample rate
}
