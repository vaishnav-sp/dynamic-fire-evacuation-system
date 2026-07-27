from app.prediction.trend_analyzer import TrendAnalyzer
from app.prediction.prediction_engine import PredictionEngine


class FirePredictor:


    def __init__(self):

        self.trend = TrendAnalyzer()

        self.engine = PredictionEngine()



    def update(
        self,
        node_id,
        hazard
    ):

        self.trend.add(
            node_id,
            hazard
        )



    def predict(
        self,
        node_id
    ):


        history = self.trend.get_history(
            node_id
        )


        if not history:

            return {

                "current":0,

                "prediction":{},

                "ignition_probability":0

            }



        current = history[-1]


        rate = self.trend.get_rate(
            node_id
        )


        predictions = self.engine.predict_future(
            current,
            rate
        )


        probability = (

            current * 0.7

            +

            max(rate,0) * 30

        )


        probability = max(
            0,
            min(
                probability,
                100
            )
        )


        return {

            "current":
                current,


            "prediction":
                predictions,


            "ignition_probability":
                round(
                    probability,
                    2
                )

        }