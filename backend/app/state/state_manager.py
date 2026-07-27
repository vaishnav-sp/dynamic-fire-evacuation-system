from app.hazard.sensor_fusion import SensorFusion
from app.prediction.fire_predictor import FirePredictor



class StateManager:


    def __init__(self):

        self.nodes = {}

        self.fusion = SensorFusion()

        self.predictor = FirePredictor()



    def get_risk(
        self,
        hazard_score,
        predicted_hazard
    ):


        risk = max(
            hazard_score,
            predicted_hazard
        )


        if risk >= 75:

            return "CRITICAL"


        elif risk >= 50:

            return "DANGER"


        elif risk >= 25:

            return "MODERATE"


        else:

            return "SAFE"




    def update(
        self,
        data
    ):


        sensor_data = {

            "temperature":
                data["temperature"],

            "smoke":
                data["smoke"],

            "flame":
                data["flame"],

            "occupancy":
                data["occupancy"]

        }



        # Current hazard calculation

        hazard_score = self.fusion.calculate(
            sensor_data
        )




        # Prediction update

        self.predictor.update(
            data["node_id"],
            hazard_score
        )



        prediction = self.predictor.predict(
            data["node_id"]
        )



        predicted_hazard = prediction[
            "ignition_probability"
        ]




        # Final risk state

        risk = self.get_risk(
            hazard_score,
            predicted_hazard
        )




        self.nodes[data["node_id"]] = {


            "node_type":
                data["node_type"],


            "temperature":
                data["temperature"],


            "smoke":
                data["smoke"],


            "flame":
                data["flame"],


            "occupancy":
                data["occupancy"],



            "hazard_score":
                round(
                    hazard_score,
                    2
                ),



            "predicted_hazard":
                predicted_hazard,



            "prediction":
                prediction["prediction"],



            "risk":
                risk,



            "health":
                data.get(
                    "health",
                    "ONLINE"
                ),



            "confidence":
                data.get(
                    "confidence",
                    100
                ),



            "hazard":
                data.get(
                    "hazard",
                    hazard_score
                )

        }




        print(
            f"\n{data['node_id']} | "
            f"Hazard={hazard_score:.2f}% | "
            f"Predicted={predicted_hazard}% | "
            f"Risk={risk}"
        )


        print(
            "Prediction:",
            prediction["prediction"]
        )


        print(
            "Ignition Probability:",
            predicted_hazard,
            "%"
        )





    def get(
        self,
        node_id
    ):

        return self.nodes.get(
            node_id
        )




    def all_nodes(self):

        return self.nodes