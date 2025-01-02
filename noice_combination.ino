#include <ESP32Servo.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include "esp_camera.h"
#include "FS.h"
#include "SD_MMC.h"
#include <EEPROM.h>

const char *ssid = "Yegorebet Lij";
const char *password = "and eske 8";

WebSocketsClient webSocket;

#define SERVO_PIN 12
#define FLASH_LED_PIN 4
#define IR_SENSOR_PIN 15
#define RED_LED_PIN 2
#define GREEN_LED_PIN 14

#define EEPROM_SIZE 1
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

Servo servo1; 
int pictureNumber = 0; 
bool sensorTriggered = false; 

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length);
void captureImage();

void setup() {
  Serial.begin(115200);

  pinMode(FLASH_LED_PIN, OUTPUT);
  pinMode(IR_SENSOR_PIN, INPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, HIGH); 

  servo1.attach(SERVO_PIN, 500, 2400);
  servo1.write(0); 

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  webSocket.begin("192.168.205.22", 8000, "/ws/esp32/");
  webSocket.onEvent(webSocketEvent);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera initialization failed");
    while (true);
  }

  if (!SD_MMC.begin()) {
    Serial.println("SD Card Mount Failed");
    while (true);
  }

  EEPROM.begin(EEPROM_SIZE);
  pictureNumber = EEPROM.read(0);
}

void loop() {
  int irSensorState = digitalRead(IR_SENSOR_PIN);

  if (irSensorState == LOW) { 
    if (!sensorTriggered) {
      sensorTriggered = true;
      digitalWrite(FLASH_LED_PIN, HIGH); 
      captureImage();
    }
  } else { 
    sensorTriggered = false;
    digitalWrite(FLASH_LED_PIN, LOW); 
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

      StaticJsonDocument<200> doc;
      if (deserializeJson(doc, payload)) {
        Serial.println("Failed to parse JSON");
        return;
      }

      const char *action = doc["action"];
      const char *rackId = doc["rackId"];
      StaticJsonDocument<200> responseDoc;

      if (strcmp(action, "lock") == 0) {
        if (strcmp(rackId, "2") == 0 && sensorTriggered) {
          servo1.write(50); 
          digitalWrite(RED_LED_PIN, HIGH); 
          digitalWrite(GREEN_LED_PIN, LOW); 
          responseDoc["action"] = "lock";
          responseDoc["status"] = "success";
        } else {
          responseDoc["action"] = "lock";
          responseDoc["status"] = "failure";
        }
      } else if (strcmp(action, "unlock") == 0) {
        if (strcmp(rackId, "2") == 0 && sensorTriggered) {
          servo1.write(0); 
          digitalWrite(RED_LED_PIN, LOW); 
          digitalWrite(GREEN_LED_PIN, HIGH); 
          responseDoc["action"] = "unlock";
          responseDoc["status"] = "success";
        } else {
          responseDoc["action"] = "unlock";
          responseDoc["status"] = "failure";
        }
      } else {
        responseDoc["action"] = "error";
        responseDoc["message"] = "Unknown action received.";
      }

      String response;
      serializeJson(responseDoc, response);
      webSocket.sendTXT(response);
      break;
    }
    default:
      break;
  }
}

void captureImage() {
  Serial.println("Capturing image...");
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  pictureNumber++;
  String path = "/picture" + String(pictureNumber) + ".jpg";
  File file = SD_MMC.open(path.c_str(), FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file for writing");
  } else {
    file.write(fb->buf, fb->len);
    Serial.printf("Image saved: %s\n", path.c_str());
    EEPROM.write(0, pictureNumber);
    EEPROM.commit();
  }
  file.close();
  esp_camera_fb_return(fb);
}

