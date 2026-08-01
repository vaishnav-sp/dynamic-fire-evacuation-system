from dataclasses import dataclass, field
from typing import Dict

from app.models.room import Room
from app.models.corridor import Corridor
from app.models.exit import Exit


@dataclass
class Building:
    name: str

    rooms: Dict[str, Room] = field(default_factory=dict)
    corridors: Dict[str, Corridor] = field(default_factory=dict)
    lobbies: Dict[str, Corridor] = field(default_factory=dict)
    exits: Dict[str, Exit] = field(default_factory=dict)

    connections: list = field(default_factory=list)

    def add_room(self, room: Room):
        self.rooms[room.id] = room

    def add_corridor(self, corridor: Corridor):
        self.corridors[corridor.id] = corridor

    def add_lobby(self, lobby: Corridor):
        self.lobbies[lobby.id] = lobby

    def add_exit(self, exit_obj: Exit):
        self.exits[exit_obj.id] = exit_obj

    def add_connection(self, connection: dict):
        self.connections.append(connection)

    def get_neighbors(self, node_id):
        return list(self.graph.neighbors(node_id))

    def get_all_nodes(self):
        nodes = {}

        nodes.update(self.rooms)
        nodes.update(self.corridors)
        nodes.update(self.lobbies)

        return nodes

    def __str__(self):
        return (
            f"\nBuilding : {self.name}\n"
            f"Rooms : {len(self.rooms)}\n"
            f"Corridors : {len(self.corridors)}\n"
            f"Lobbies : {len(self.lobbies)}\n"
            f"Exits : {len(self.exits)}\n"
            f"Connections : {len(self.connections)}"
        )