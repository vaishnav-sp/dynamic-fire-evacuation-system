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

        graph = self.graph.copy()

        protected = set(exits)
        protected.add(start)

        graph.remove_nodes_from(
            [n for n in blocked_nodes if n not in protected]
        )

        best_route = None
        best_score = float("inf")

        for exit_node in exits:

            if exit_node not in graph:
                continue

            try:

                # Get several possible routes
                paths = nx.shortest_simple_paths(
                    graph,
                    start,
                    exit_node,
                    weight="cost"
                )

                checked = 0

                for path in paths:

                    checked += 1

                    if checked > 10:
                        break

                    edge_cost = 0
                    cumulative_risk = 0
                    max_risk = 0
                    danger_nodes = 0

                    for i in range(len(path) - 1):

                        edge = graph[path[i]][path[i + 1]]

                        edge_cost += edge["cost"]

                    for node in path:

                        risk = 0

                        for nbr in graph.neighbors(node):

                            edge = graph[node][nbr]

                            risk = max(
                                risk,
                                edge["cost"] - edge["distance"]
                            )

                        cumulative_risk += risk
                        max_risk = max(max_risk, risk)

                        if risk > 30:
                            danger_nodes += 1

                    score = (
                        edge_cost
                        + cumulative_risk * 2
                        + max_risk * 10
                        + danger_nodes * 100
                    )

                    if score < best_score:

                        best_score = score

                        best_route = {
                            "path": path,
                            "cost": round(edge_cost, 2)
                        }

            except nx.NetworkXNoPath:
                continue

        if best_route is None:
            return {
                "type": "SAFEST",
                "path": None,
                "cost": None,
                "reason": "No safe route available"
            }

        return {
            "type": "SAFEST",
            "path": best_route["path"],
            "cost": best_route["cost"],
            "reason": "Lowest cumulative fire-risk path selected"
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