import time


class HazardMap:

    def __init__(self):

        self.nodes = {}


    def update(self, node_id, data):

        hazard = data.get(
            "hazard",
            0
        )

        prediction = data.get(
            "prediction",
            {}
        )


        prediction_score = self.get_prediction_score(
            prediction
        )


        self.nodes[node_id] = {

            "temperature": data.get(
                "temperature",
                0
            ),

            "smoke": data.get(
                "smoke",
                0
            ),

            "flame": data.get(
                "flame",
                0
            ),

            "occupancy": data.get(
                "occupancy",
                0
            ),


            # Current hazard
            "hazard": hazard,


            # Future hazard
            "prediction": prediction,


            "prediction_score": prediction_score,


            # Risk category
            "risk": self.calculate_risk(
                hazard
            ),


            # Sensor reliability
            "confidence": self.calculate_confidence(
                data
            ),


            # Communication health
            "sensor_status": "ONLINE",


            "last_update": time.time()

        }



    def get_prediction_score(self, prediction):

        if not prediction:
            return 0


        values = list(
            prediction.values()
        )


        if len(values)==0:
            return 0


        return max(values)



    def calculate_risk(self, hazard):

        if hazard < 20:

            return "SAFE"


        elif hazard < 40:

            return "MODERATE"


        elif hazard < 70:

            return "DANGER"


        else:

            return "CRITICAL"



    def calculate_confidence(self,data):

        confidence = 100


        required = [

            "temperature",

            "smoke",

            "flame",

            "occupancy"

        ]


        for item in required:

            if data.get(item) is None:

                confidence -= 20



        return max(
            confidence,
            0
        )



    def get_map(self):

        return self.nodes