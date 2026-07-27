from app.prediction.trend_analyzer import TrendAnalyzer


class FirePredictor:


    def __init__(self):

        self.trend = TrendAnalyzer()



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

        rate = self.trend.get_rate(
            node_id
        )


        current = self.trend.history[node_id][-1]


        predictions = {}



        for seconds in [30, 60, 90]:


            future = current + (
                rate * seconds
            )


            if future > 100:

                future = 100


            if future < 0:

                future = 0



            predictions[
                f"{seconds}s"
            ] = round(
                future,
                2
            )



        # Use 60 second prediction as future risk

        trend_prediction = predictions["60s"]



        ignition_probability = min(

            (
                current * 0.5
                +
                trend_prediction * 0.5
            ),

            100

        )



        return {

            "current":
                current,


            "prediction":
                predictions,


            "ignition_probability":
                round(
                    ignition_probability,
                    2
                )

        }