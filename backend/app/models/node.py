from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class Node:
    id: str
    name: str
    node_type: str  # REAL or VIRTUAL

    # Sensor Data
    temperature: float = 0.0
    smoke: float = 0.0
    flame: bool = False
    occupancy: int = 0

    # Hazard Information
    hazard_score: float = 0.0
    predicted_hazard: float = 0.0
    confidence: float = 100.0

    # Status
    state: str = "SAFE"
    sensor_online: bool = True

    # Graph
    neighbors: List[str] = field(default_factory=list)

    # Time
    last_updated: datetime = field(default_factory=datetime.now)

    def update_timestamp(self):
        self.last_updated = datetime.now()