import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ESP32Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("ESP32 connected!")

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        print("ESP32 disconnected!")

    async def receive(self, text_data):
        # Handle incoming WebSocket message
        data = json.loads(text_data)
        print("Received from ESP32:", data)

        # Send response back to ESP32
        await self.send(text_data=json.dumps({
            'response': 'Message received!'
        }))
