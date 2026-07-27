class WeightEngine:


    @staticmethod
    def calculate(edge, hazard_map):


        source = hazard_map.get(
            edge["from"],
            {}
        )


        target = hazard_map.get(
            edge["to"],
            {}
        )


        distance = edge["distance"]


        source_risk = (
            source.get("hazard_score",0)*0.4
            +
            source.get("predicted_hazard",0)*0.6
        )


        target_risk = (
            target.get("hazard_score",0)*0.4
            +
            target.get("predicted_hazard",0)*0.6
        )


        risk = (
            source_risk +
            target_risk
        ) / 2



        occupancy = (
            source.get("occupancy",0)
            +
            target.get("occupancy",0)
        ) / 2



        confidence = (
            source.get("confidence",100)
            +
            target.get("confidence",100)
        ) / 2



        confidence_penalty = (
            100-confidence
        )*0.2



        cost = (

            distance

            +

            risk*0.6

            +

            occupancy*0.5

            +

            confidence_penalty

        )


        if risk > 80:

            cost += 200


        return round(cost,2)