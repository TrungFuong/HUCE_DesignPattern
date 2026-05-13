import asyncio
from typing import Callable

import paho.mqtt.client as mqtt


class HiveMqttClient:

    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self.client = mqtt.Client()
        self._loop = asyncio.get_event_loop()

    async def connect(self) -> None:
        self.client.connect_async(self.broker_url)
        self.client.loop_start()

    async def subscribe(self, topic: str, callback: Callable[[object], None]) -> None:
        def on_message(client, userdata, message):
            self._loop.call_soon_threadsafe(lambda: self._loop.create_task(callback(message)))

        self.client.subscribe(topic)
        self.client.on_message = on_message
