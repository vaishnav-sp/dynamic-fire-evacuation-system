from app.models.sensor import Sensor
from app.models.sensor_packet import SensorPacket
from app.mqtt.publisher import Publisher
from app.mqtt.topics import ROOM_TOPIC

publisher = Publisher()

publisher.connect()

packet = SensorPacket(

    node_id="R1",

    node_type="REAL",

    sensor=Sensor(

        temperature=32,

        smoke=18,

        flame=False,

        occupancy=4

    )

)

publisher.publish(ROOM_TOPIC, packet)

print("Published")