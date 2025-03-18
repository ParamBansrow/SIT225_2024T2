
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>

// WiFi Credentials
const char* ssid = "Param";
const char* password = "aus@2112";

// HiveMQ Credentials
const char* mqttServer = "e42ea22cdfca44c9a56ff4d6bd9b1b13.s1.eu.hivemq.cloud";
const int mqttPort = 8883;
const char* mqttUser = "hivemq.webclient.1742118867901";
const char* mqttPassword = "9832IYJKZpabAncd,.?&";
const char* topic = "gyro/data";

WiFiSSLClient wifiClient;
PubSubClient mqttClient(wifiClient);

void setup() {
    Serial.begin(115200);
    while (!Serial);

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("WiFi connected!");

    // Setup MQTT
   
    mqttClient.setServer(mqttServer, mqttPort);
    if (!mqttClient.connect("ArduinoClient", mqttUser, mqttPassword)) {
        Serial.println("MQTT connection failed!");
        return;
    }
    Serial.println("Connected to MQTT broker!");

    // Initialize gyroscope sensor
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
}

void loop() {
    float x, y, z;
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);

        // Create JSON message
        String payload = "{";
        payload += "\"x\":" + String(x, 3) + ",";
        payload += "\"y\":" + String(y, 3) + ",";
        payload += "\"z\":" + String(z, 3);
        payload += "}";

        // Publish to MQTT
        mqttClient.publish(topic, payload.c_str());
        Serial.println("Published: " + payload);

        delay(1000); // Adjust as needed
    }
}

