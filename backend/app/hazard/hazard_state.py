from dataclasses import dataclass


@dataclass
class HazardState:

    temperature: float = 25

    smoke: float = 0

    flame: bool = False

    fire_intensity: float = 0

    spread_probability: float = 0