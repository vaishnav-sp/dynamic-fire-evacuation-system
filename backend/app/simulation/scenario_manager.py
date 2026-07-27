from app.hazard.fire_node import FireNode


class ScenarioManager:

    def __init__(self):

        self.nodes = {}

    def initialize(self, building):

        for room in building.rooms:

            self.nodes[room] = FireNode(room)

        for corridor in building.corridors:

            self.nodes[corridor] = FireNode(corridor)

    def ignite(self, node):

        self.nodes[node].flame = True

        self.nodes[node].fire_intensity = 5

    def get(self, node):

        return self.nodes[node]

    def all_nodes(self):

        return self.nodes.values()