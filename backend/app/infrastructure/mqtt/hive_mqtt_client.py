import asyncio
from typing import Callable
from urllib.parse import urlparse

import paho.mqtt.client as mqtt


class HiveMqttClient:

    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self.client = mqtt.Client()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._connected = asyncio.Event()

    async def connect_and_subscribe(
        self, topic: str, callback: Callable[[object], None]
    ) -> None:
        """Connect to broker and subscribe to topic using on_connect callback (correct pattern)."""
        loop = asyncio.get_running_loop()
        self._loop = loop
        self._connected = asyncio.Event()

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"[MQTT] Connected to broker successfully (rc=0)")
                client.subscribe(topic)
                print(f"[MQTT] Subscribed to topic: {topic}")
                loop.call_soon_threadsafe(self._connected.set)
            else:
                print(f"[MQTT] Connection failed (rc={rc})")

        def on_message(client, userdata, message):
            print(f"[MQTT] Raw message received on topic: {message.topic}")
            asyncio.run_coroutine_threadsafe(callback(message), loop)

        def on_disconnect(client, userdata, rc):
            print(f"[MQTT] Disconnected (rc={rc}), reconnecting...")
            loop.call_soon_threadsafe(self._connected.clear)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

        host, port = self._parse_broker_url(self.broker_url)
        print(f"[MQTT] Connecting to {host}:{port} ...")
        self.client.connect_async(host, port)
        self.client.loop_start()

        # Wait up to 10s for connection
        try:
            await asyncio.wait_for(self._connected.wait(), timeout=10.0)
            print(f"[MQTT] Ready. Listening on topic: {topic}")
        except asyncio.TimeoutError:
            print(f"[MQTT] WARNING: Connection timeout after 10s, continuing anyway...")

    # Keep old methods for backward compat
    async def connect(self) -> None:
        self._loop = asyncio.get_running_loop()
        host, port = self._parse_broker_url(self.broker_url)
        self.client.connect_async(host, port)
        self.client.loop_start()

    async def subscribe(self, topic: str, callback: Callable[[object], None]) -> None:
        loop = self._loop or asyncio.get_running_loop()

        def on_message(client, userdata, message):
            print(f"[MQTT] Raw message received on topic: {message.topic}")
            asyncio.run_coroutine_threadsafe(callback(message), loop)

        self.client.subscribe(topic)
        self.client.on_message = on_message
        print(f"[MQTT] Subscribed to topic: {topic}")

    @staticmethod
    def _parse_broker_url(broker_url: str) -> tuple[str, int]:
        parsed = urlparse(broker_url)
        if parsed.scheme in ("mqtt", "tcp", "ssl") and parsed.hostname:
            port = parsed.port or 1883
            return parsed.hostname, port
        if ":" in broker_url:
            host, port_str = broker_url.split(":", 1)
            return host, int(port_str)
        return broker_url, 1883
