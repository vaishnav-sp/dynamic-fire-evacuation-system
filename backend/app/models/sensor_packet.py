from dataclasses import dataclass
import json
import time

from app.models.sensor import Sensor


@dataclass
class SensorPacket:

    node_id: str
    node_type: str
    sensor: Sensor

    timestamp: float = 0
    health: str = "ONLINE"
    confidence: float = 1.0

    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

    def to_json(self):

        return json.dumps({

            "node_id": self.node_id,
            "node_type": self.node_type,

            "temperature": self.sensor.temperature,
            "smoke": self.sensor.smoke,
            "flame": self.sensor.flame,
            "occupancy": self.sensor.occupancy,

            "timestamp": self.timestamp,
            "health": self.health,
            "confidence": self.confidence

        })

    @staticmethod
    def from_json(data):

        obj = json.loads(data)

        return SensorPacket(

            node_id=obj["node_id"],
            node_type=obj["node_type"],

            sensor=Sensor(

                temperature=obj["temperature"],
                smoke=obj["smoke"],
                flame=obj["flame"],
                occupancy=obj["occupancy"]

            ),

            timestamp=obj.get("timestamp", time.time()),
            health=obj.get("health", "ONLINE"),
            confidence=obj.get("confidence", 1.0)

        )

    def __str__(self):

        return (
            f"{self.node_id} | "
            f"T={self.sensor.temperature:.1f}°C | "
            f"S={self.sensor.smoke:.1f} | "
            f"F={self.sensor.flame:.1f} | "
            f"O={self.sensor.occupancy}"
        )