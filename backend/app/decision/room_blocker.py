class RoomBlocker:


    BLOCK_THRESHOLD = 70



    def get_blocked_nodes(
        self,
        hazard_map
    ):


        blocked = []



        for node_id, data in hazard_map.items():


            hazard = data.get(
                "hazard_score",
                0
            )


            prediction = data.get(
                "predicted_hazard",
                0
            )



            # Combined current + future risk
            risk = (
                hazard * 0.4
                +
                prediction * 0.6
            )



            if risk >= self.BLOCK_THRESHOLD:

                blocked.append(
                    node_id
                )



        return blocked