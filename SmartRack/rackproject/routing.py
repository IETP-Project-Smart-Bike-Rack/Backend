from django.urls import path
from . import consumers

websocket_urlpattern = [
    path("ws/esp32/", consumers.ESP32Consumer.as_asgi()),
]