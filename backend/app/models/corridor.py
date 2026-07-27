from dataclasses import dataclass

from app.models.node import Node



@dataclass
class Corridor(Node):

    led_direction: str = "OFF"



    def __str__(self):

        return (

            f"{self.id} | "

            f"{self.state} | "

            f"LED={self.led_direction} | "

            f"Temp={self.temperature:.1f}°C | "

            f"Smoke={self.smoke:.1f}"

        )