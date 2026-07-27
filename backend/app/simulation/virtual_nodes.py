from app.models.sensor import Sensor
from app.models.sensor_packet import SensorPacket

from app.mqtt.publisher import Publisher
from app.mqtt.topics import node_topic

class VirtualNodes:

    def __init__(self):

        self.publisher = Publisher()

        self.publisher.connect()

    def publish(self, node_id, node_type, profile, occupancy):

        packet = SensorPacket(

            node_id=node_id,

            node_type=node_type,

            sensor=Sensor(

                temperature=profile["temperature"],

                smoke=profile["smoke"],

                flame=profile["flame"],

                occupancy=occupancy

            )

        )

        topic = node_topic(node_id)

        self.publisher.publish(topic, packet)