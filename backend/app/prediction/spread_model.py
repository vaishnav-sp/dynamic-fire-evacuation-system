class SpreadModel:


    def __init__(self):

        self.spread_factor = 0.15



    def calculate_spread(
        self,
        hazard,
        distance
    ):

        spread = hazard * self.spread_factor


        if distance > 0:

            spread = spread / distance


        return round(
            min(spread,100),
            2
        )