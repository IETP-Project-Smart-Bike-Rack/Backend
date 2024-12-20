import json
from channels.generic.websocket import WebsocketConsumer

class ESP32Consumer(WebsocketConsumer):
    esp_socket = None

    def connect(self):
        self.accept()
        ESP32Consumer.esp_socket = self
        print("WebSocket connect")
    
    def recieve(self, text_data):
        data = json.loads(text_data)
        print(f"Recieved: {data}")