import random


class OccupancySimulator:

    def __init__(self):

        self.occupancy = {}

    def initialize(self, building):

        for room in building.rooms.values():
            self.occupancy[room.id] = random.randint(0, 5)

        for corridor in building.corridors.values():
            self.occupancy[corridor.id] = random.randint(0, 3)

    def update(self):

        for node in self.occupancy:

            change = random.choice([-1, 0, 1])

            self.occupancy[node] = max(
                0,
                self.occupancy[node] + change
            )

    def get(self, node_id):

        return self.occupancy.get(node_id, 0)