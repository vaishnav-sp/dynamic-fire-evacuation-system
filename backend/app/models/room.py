from dataclasses import dataclass

from app.models.node import Node



@dataclass
class Room(Node):


    def __str__(self):

        return (

            f"{self.id} | "

            f"{self.state} | "

            f"Temp={self.temperature:.1f}°C | "

            f"Smoke={self.smoke:.1f} | "

            f"Occupancy={self.occupancy}"

        )