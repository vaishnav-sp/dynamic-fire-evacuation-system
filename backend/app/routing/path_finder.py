import networkx as nx



class PathFinder:


    def __init__(self, graph):

        self.graph = graph



    def find_safest_path(
        self,
        start,
        exits,
        blocked_nodes=None
    ):


        if blocked_nodes is None:

            blocked_nodes = []



        if start not in self.graph:

            return {

                "type": "SAFEST",

                "path": None,

                "cost": None,

                "reason": "Starting node not found"

            }



        if not exits:

            return {

                "type": "SAFEST",

                "path": None,

                "cost": None,

                "reason": "No exits available"

            }



        # Copy graph to preserve original

        graph = self.graph.copy()



        # Never block current position

        # Never block exits

        protected_nodes = set(exits)

        protected_nodes.add(start)



        removable_nodes = [

            node

            for node in blocked_nodes

            if node not in protected_nodes

        ]



        graph.remove_nodes_from(
            removable_nodes
        )



        best_path = None

        best_cost = float("inf")



        for exit_node in exits:


            if exit_node not in graph:

                continue



            try:


                path = nx.dijkstra_path(

                    graph,

                    start,

                    exit_node,

                    weight="cost"

                )



                cost = nx.dijkstra_path_length(

                    graph,

                    start,

                    exit_node,

                    weight="cost"

                )



                if cost < best_cost:

                    best_cost = cost

                    best_path = path



            except nx.NetworkXNoPath:

                continue




        if best_path is None:

            return {

                "type": "SAFEST",

                "path": None,

                "cost": None,

                "reason": "No safe path available"

            }




        return {


            "type": "SAFEST",


            "path": best_path,


            "cost": round(
                best_cost,
                2
            ),


            "reason":
                "Safest hazard-aware route selected"

        }





    def find_shortest_path(
        self,
        start,
        exits,
        blocked_nodes=None
    ):


        if blocked_nodes is None:

            blocked_nodes = []



        if start not in self.graph:

            return {

                "type": "SHORTEST",

                "path": None,

                "distance": None,

                "reason": "Starting node not found"

            }



        if not exits:

            return {

                "type": "SHORTEST",

                "path": None,

                "distance": None,

                "reason": "No exits available"

            }



        # Copy graph to preserve original

        graph = self.graph.copy()



        # Never block current position

        # Never block exits

        protected_nodes = set(exits)

        protected_nodes.add(start)



        removable_nodes = [

            node

            for node in blocked_nodes

            if node not in protected_nodes

        ]



        graph.remove_nodes_from(

            removable_nodes

        )



        best_path = None

        best_distance = float("inf")



        for exit_node in exits:


            if exit_node not in graph:

                continue



            try:


                path = nx.dijkstra_path(

                    graph,

                    start,

                    exit_node,

                    weight="distance"

                )



                distance = nx.dijkstra_path_length(

                    graph,

                    start,

                    exit_node,

                    weight="distance"

                )



                if distance < best_distance:

                    best_distance = distance

                    best_path = path



            except nx.NetworkXNoPath:

                continue





        if best_path is None:

            return {

                "type": "SHORTEST",

                "path": None,

                "distance": None,

                "reason": "No path exists"

            }




        return {


            "type": "SHORTEST",


            "path": best_path,


            "distance": round(

                best_distance,

                2

            ),


            "reason":

                "Shortest distance route selected"

        }