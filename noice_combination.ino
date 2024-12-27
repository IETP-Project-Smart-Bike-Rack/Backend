#include <ESP32Servo.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

const char *ssid = "TCL 30 SE 7893";
const char *password = "11121314";

WebSocketsClient webSocket;

// Define a single Servo object
Servo servo1;

// Define GPIO pin for the servo
#define SERVO_PIN_1 12
#define FLASH_LED_PIN 4
#define IR_SENSOR_PIN 15 // Replace with the pin number where your IR sensor's output is connected
#define FLASH_LED_PIN 4  // ESP32-CAM's flash LED pin


void setup() {
  Serial.begin(115200);

  pinMode(FLASH_LED_PIN, OUTPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  }

  // Initialize WebSocket
  // webSocket.begin("192.168.223.61", 8000, "/ws/esp32/");
  webSocket.begin("192.168.173.22", 8000, "/ws/esp32/");
  // webSocket.begin("192.168.67.198", 8000, "/ws/esp32/");
  webSocket.onEvent(webSocketEvent);

  // Attach the servo to its GPIO pin
  servo1.attach(SERVO_PIN_1, 500, 2400);

  pinMode(IR_SENSOR_PIN, INPUT);   // Set the IR sensor pin as input
  pinMode(FLASH_LED_PIN, OUTPUT); // Set the flash LED pin as output

  digitalWrite(FLASH_LED_PIN, LOW); // Ensure the flash is initially off
  
}

bool sensor = false;

void loop() {
  int irSensorState = digitalRead(IR_SENSOR_PIN); // Read IR sensor state
  
  // Invert the condition: Object detected if LOW
  if (irSensorState == LOW) { // Object detected
  sensor = true;
    digitalWrite(FLASH_LED_PIN, HIGH); // Turn on the flash
    // Serial.println("Object detected - Flashlight ON");
  } else { // No object detected
  sensor = false;
    digitalWrite(FLASH_LED_PIN, LOW); // Turn off the flash
    // Serial.println("No object detected - Flashlight OFF");
  }

  webSocket.loop();
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_CONNECTED:
      Serial.println("WebSocket Connected");
      break;

    case WStype_DISCONNECTED:
      Serial.println("WebSocket Disconnected");
      break;

    case WStype_TEXT: {
      Serial.printf("Received: %s\n", payload);

      // Parse JSON payload
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, payload);

      if (error) {
        Serial.println("Failed to parse JSON");
        return;
      }

      const char *action = doc["action"];
      const char *rackId = doc["rackId"];

      if (!action ) {
        Serial.println("Invalid JSON format: Missing 'action' ");
        return;
      }

      if (!rackId) {
        Serial.println("Invalid JSON format: Missing 'rackId'");
        return;
      }

      // Create a response JSON document to send back
      StaticJsonDocument<200> responseDoc;

      if (strcmp(action, "lock") == 0) {
        Serial.printf("Lock command received for Rack ID: %s\n", rackId);

        if (strcmp(rackId, "2") == 0 && sensor) {
          servo1.write(180); // Move servo to locked position
          Serial.println("Servo locked");

          // Send feedback to backend (Django)
          responseDoc["action"] = "lock";
          responseDoc["status"] = "success";
          responseDoc["rackId"] = rackId;
          responseDoc["message"] = "Rack locked successfully!";
        } else {
          Serial.println("Invalid Rack ID or sensor not triggered for lock command");

          // Send feedback to backend (Django)
          responseDoc["action"] = "lock";
          responseDoc["status"] = "failure";
          responseDoc["rackId"] = rackId;
          responseDoc["message"] = "Failed to lock the rack. Ensure sensor detects an object.";
        }

      } else if (strcmp(action, "unlock") == 0) {
        Serial.printf("Unlock command received for Rack ID: %s\n", rackId);

        if (strcmp(rackId, "2") == 0 && sensor) {
          servo1.write(0); // Move servo to unlocked position
          Serial.println("Servo unlocked");

          // Send feedback to backend (Django)
          responseDoc["action"] = "unlock";
          responseDoc["status"] = "success";
          responseDoc["rackId"] = rackId;
          responseDoc["message"] = "Rack unlocked successfully!";
        } else {
          Serial.println("Invalid Rack ID or sensor not triggered for unlock command");

          // Send feedback to backend (Django)
          responseDoc["action"] = "unlock";
          responseDoc["status"] = "failure";
          responseDoc["rackId"] = rackId;
          responseDoc["message"] = "Failed to unlock the rack. Ensure sensor detects an object.";
        }
      } else {
        Serial.println("Unknown action");

        // Send feedback to backend (Django) for unknown action
        responseDoc["action"] = "error";
        responseDoc["message"] = "Unknown action received.";
      }

      // Convert the response to a string and send it to Django (backend)
      String responseMessage;
      serializeJson(responseDoc, responseMessage);
      webSocket.sendTXT(responseMessage); // Send the message to Django backend via WebSocket

      break;
    }

    default:
      break;
  }
}




// ////////////////////////////////////////////////////////////////////////////////////
