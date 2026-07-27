class FireNode:


    def __init__(
        self,
        node_id
    ):

        self.node_id = node_id


        # Fire parameters

        self.temperature = 25

        self.smoke = 0

        self.flame = False

        self.fire_intensity = 0



        # Existing system compatibility

        self.occupancy = 0

        self.hazard_score = 0

        self.spread_probability = 0



        # Metadata

        self.state = "SAFE"



    def ignite(self):

        self.flame = True

        self.fire_intensity = 5

        self.temperature = max(
            self.temperature,
            60
        )

        self.smoke = max(
            self.smoke,
            20
        )