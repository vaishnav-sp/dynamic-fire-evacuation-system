class DecisionEngine:

    EVACUATION_THRESHOLD = 50
    CRITICAL_THRESHOLD = 75


    def evaluate(self, hazard_map):

        critical_nodes = []

        evacuation_required = False


        for node_id, data in hazard_map.items():


            current_hazard = data.get(
                "hazard_score",
                0
            )


            predicted_hazard = data.get(
                "predicted_hazard",
                0
            )


            risk_score = (
                current_hazard * 0.4
                +
                predicted_hazard * 0.6
            )



            if risk_score >= self.EVACUATION_THRESHOLD:

                evacuation_required = True



            if risk_score >= self.CRITICAL_THRESHOLD:

                critical_nodes.append(
                    node_id
                )



        return {

            "evacuation_required":
                evacuation_required,


            "critical_nodes":
                critical_nodes,


            "reason":
                self.get_reason(
                    evacuation_required,
                    critical_nodes
                )

        }



    def get_reason(
        self,
        evacuation,
        critical
    ):


        if critical:

            return (
                "Critical fire hazard detected in "
                +
                ",".join(critical)
            )


        if evacuation:

            return (
                "High predicted fire risk detected"
            )


        return (
            "Building conditions normal"
        )