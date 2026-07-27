from dataclasses import dataclass


@dataclass
class Sensor:
    temperature: float
    smoke: float
    flame: bool
    occupancy: int