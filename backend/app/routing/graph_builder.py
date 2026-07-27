import json
import networkx as nx

from app.models.building import Building
from app.models.room import Room
from app.models.corridor import Corridor
from app.models.exit import Exit


class GraphBuilder:


    def __init__(self, building_file):

        self.building_file = building_file

        self.graph = nx.Graph()



    def load(self):

        with open(
            self.building_file,
            "r"
        ) as file:

            data = json.load(file)



        # Create building object
        # Supports both "name" and "building_name"

        building_name = data.get(
            "name",
            data.get(
                "building_name",
                "Unknown Building"
            )
        )


        building = Building(
            building_name
        )



        # -----------------------
        # Rooms
        # -----------------------

        for room in data["rooms"]:


            obj = Room(

                id=room["id"],

                name=room["name"],

                node_type=room.get(
                    "node_type",
                    room.get(
                        "type",
                        "VIRTUAL"
                    )
                )

            )


            building.add_room(
                obj
            )


            self.graph.add_node(

                obj.id,

                type="ROOM"

            )



        # -----------------------
        # Corridors
        # -----------------------

        for corridor in data["corridors"]:


            obj = Corridor(

                id=corridor["id"],

                name=corridor["name"],

                node_type=corridor.get(
                    "node_type",
                    corridor.get(
                        "type",
                        "VIRTUAL"
                    )
                )

            )


            building.add_corridor(
                obj
            )


            self.graph.add_node(

                obj.id,

                type="CORRIDOR"

            )



        # -----------------------
        # Exits
        # -----------------------

        for exit_node in data["exits"]:


            obj = Exit(

                id=exit_node["id"],

                name=exit_node["name"]

            )


            building.add_exit(
                obj
            )


            self.graph.add_node(

                obj.id,

                type="EXIT"

            )



        # -----------------------
        # Connections
        # -----------------------

        for edge in data["connections"]:


            building.add_connection(
                edge
            )


            self.graph.add_edge(

                edge["from"],

                edge["to"],

                distance=edge["distance"],

                cost=edge["distance"]

            )



        building.graph = self.graph


        return building, self.graph