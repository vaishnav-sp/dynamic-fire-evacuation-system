import paho.mqtt.client as mqtt

from app.config.settings import MQTT_BROKER
from app.config.constants import MQTT_PORT

from app.models.sensor_packet import SensorPacket


class MQTTManager:

    def __init__(self, building_manager):

        self.building_manager = building_manager

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):

        self.client.connect(MQTT_BROKER, MQTT_PORT)

    def start(self):

        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):

        print("MQTT Connected")

        client.subscribe("fire/#")

    def on_message(self, client, userdata, msg):

        packet = SensorPacket.from_json(
            msg.payload.decode()
        )

        self.building_manager.update_node(packet)