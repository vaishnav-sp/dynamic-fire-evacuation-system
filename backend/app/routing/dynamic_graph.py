from app.routing.weight_engine import WeightEngine


class DynamicGraph:


    def __init__(self, graph):

        self.graph = graph



    def update_weights(self, hazard_map):

        for source, target, data in self.graph.edges(data=True):


            edge = {

                "from": source,

                "to": target,

                "distance": data["distance"]

            }


            data["cost"] = WeightEngine.calculate(

                edge,

                hazard_map

            )



    def get_graph(self):

        return self.graph