from app.mqtt.client import create_client

class Publisher:

    def __init__(self):
        self.client = create_client()

    def connect(self):
        self.client.connect("localhost", 1883)

    def publish(self, topic, packet):
        print(f"Publishing -> {topic}")
        self.client.publish(topic, packet.to_json())