from app.hazard.fire_engine import FireEngine


class PropagationEngine:


    IGNITION_THRESHOLD = 60


    HEAT_TRANSFER = 2.5

    SMOKE_TRANSFER = 2



    def __init__(
        self,
        building,
        scenario
    ):

        self.building = building

        self.scenario = scenario



    def update(self):


        active_nodes = []


        for node in self.scenario.all_nodes():

            if getattr(node,"flame",False):

                active_nodes.append(node)



        for node in active_nodes:


            FireEngine.update(
                node
            )


            neighbors = self.building.get_neighbors(
                node.node_id
            )


            for neighbor_id in neighbors:


                target = self.scenario.get(
                    neighbor_id
                )


                if target is None:

                    continue



                self.transfer(
                    node,
                    target
                )




    def transfer(
        self,
        source,
        target
    ):


        target.temperature += (
            self.HEAT_TRANSFER
        )


        target.smoke += (
            self.SMOKE_TRANSFER
        )



        source_intensity = getattr(
            source,
            "fire_intensity",
            0
        )



        target.fire_intensity += (
            source_intensity * 0.05
        )



        if target.fire_intensity >= self.IGNITION_THRESHOLD:


            FireEngine.ignite(
                target
            )