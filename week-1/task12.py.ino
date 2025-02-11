const int ledPin = 13; // Built-in LED pin
int blinkCount = 0;

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600); // Start serial communication at 9600 baud
    while (!Serial) {
        // Wait for serial port to connect
    }
}

void loop() {
    if (Serial.available() > 0) {
        blinkCount = Serial.parseInt(); // Read the integer sent from Python
        if (blinkCount > 0) {
            Serial.println("Blinking LED " + String(blinkCount) + " times.");
            for (int i = 0; i < blinkCount; i++) {
                digitalWrite(ledPin, HIGH);
                delay(1000); // 1-second ON
                digitalWrite(ledPin, LOW);
                delay(1000); // 1-second OFF
            }

            int randomDelay = random(1, 5); // Generate a random number (1-4)
            Serial.println(randomDelay);
        }
    }
}
