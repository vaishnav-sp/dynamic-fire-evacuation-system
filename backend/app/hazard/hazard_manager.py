class HazardManager:

    def __init__(self):

        self.map = HazardMap()


    def process(self,node):

        HazardEngine.update(node)

        PredictionEngine.update(node)


        self.map.update(
            node.node_id,
            {
                "temperature": node.temperature,
                "smoke": node.smoke,
                "flame": node.flame,
                "occupancy": node.occupancy,
                "hazard": node.hazard_score,
                "prediction": node.prediction
            }
        )