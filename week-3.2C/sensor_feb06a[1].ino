#include "arduino_secrets.h"
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "thingProperties.h"

// WiFi connection details
const char SSID[] = SECRET_SSID;     // Network SSID (name)
const char PASS[] = SECRET_OPTIONAL_PASS;  // Network password (use for WPA, or use as key for WEP)

// Pin definitions for the ultrasonic sensor
const int trigPin = 9;
const int echoPin = 10;
int threshold = 100;

// Define the cloud properties
CloudFloat distance;
CloudBool alarm_triggered;

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

void setup() {
    Serial.begin(115200);
    
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    
    initProperties(); // Initialize IoT Cloud properties
    ArduinoCloud.begin(ArduinoIoTPreferredConnection);  // Begin cloud connection
    
    setDebugMessageLevel(2);
    ArduinoCloud.printDebugInfo();  // Print debugging info to serial monitor
}

void loop() {
    ArduinoCloud.update();  // Update the IoT Cloud
    
    measureDistance();      // Measure distance using ultrasonic sensor

    // Check distance and trigger alarm if threshold is met
    if (distance < threshold) {
        alarm_triggered = true;  
    } else {
        alarm_triggered = false;
    }
}

// Function to measure distance using Ultrasonic Sensor
void measureDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;  // Calculate the distance

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
}

// Define onAlarmTriggeredChange() to handle alarm state changes
void onAlarmTriggeredChange() {
    Serial.println("Alarm state changed!");
}

// Function called when the cloud distance property is updated
void onDistanceChange()  {
    if (distance < threshold) {
        alarm_triggered = true;
        // Additional action could be added here, like triggering an alert or taking other actions
    } else {
        alarm_triggered = false;
    }
}

// Cloud Property Initialization
void initProperties(){
    // Add properties to Arduino IoT Cloud, specify their types and change triggers
    ArduinoCloud.addProperty(distance, READWRITE, ON_CHANGE, onDistanceChange, 100);
    ArduinoCloud.addProperty(alarm_triggered, READWRITE, ON_CHANGE, onAlarmTriggeredChange);
}