from app.routing.dynamic_graph import DynamicGraph
from app.routing.path_finder import PathFinder



class RouteManager:


    def __init__(self, graph):

        self.dynamic_graph = DynamicGraph(
            graph
        )

        self.path_finder = PathFinder(
            graph
        )

        self.current_routes = {}



    def update(
        self,
        hazard_map
    ):

        self.dynamic_graph.update_weights(
            hazard_map
        )



        # Sync updated graph weights

        self.path_finder.graph = (
            self.dynamic_graph.get_graph()
        )



    def calculate_route(
        self,
        start,
        exits,
        blocked_nodes=None
    ):


        if blocked_nodes is None:

            blocked_nodes = []



        graph = self.dynamic_graph.get_graph()


        self.path_finder.graph = graph



        # --------------------------------
        # First attempt:
        # Safest dynamic route
        # --------------------------------

        route = self.path_finder.find_safest_path(

            start,

            exits,

            blocked_nodes

        )



        route["start"] = start

        route["blocked_nodes"] = blocked_nodes



        # --------------------------------
        # Fallback:
        # shortest available route
        # --------------------------------

        if route["path"] is None:


            route = self.path_finder.find_shortest_path(

                start,

                exits,

                blocked_nodes

            )


            route["fallback"] = True

            route["reason"] = "No safe route available, using shortest path"



        else:


            route["fallback"] = False

            route["fallback"] = False
            route["reason"] = "Safest evacuation path selected"



        self.current_routes[start] = route



        return route



    def get_current_route(
        self,
        start
    ):

        return self.current_routes.get(
            start
        )