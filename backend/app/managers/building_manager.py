from app.models.building import Building


class BuildingManager:

    current_building = None


    def __init__(self, building: Building):

        self.building = building

        BuildingManager.current_building = building



    def update_node(self, packet):

        node_id = packet.node_id


        if node_id in self.building.rooms:

            node = self.building.rooms[node_id]


        elif node_id in self.building.corridors:

            node = self.building.corridors[node_id]


        else:

            return


        node.temperature = packet.sensor.temperature

        node.smoke = packet.sensor.smoke

        node.flame = packet.sensor.flame

        node.occupancy = packet.sensor.occupancy


        node.update_timestamp()


        print(node)



    @staticmethod
    def get_building():

        return BuildingManager.current_building