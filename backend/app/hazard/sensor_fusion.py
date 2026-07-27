from app.hazard.weights import (
    TEMPERATURE_WEIGHT,
    SMOKE_WEIGHT,
    FLAME_WEIGHT,
    OCCUPANCY_WEIGHT,
    MAX_TEMPERATURE,
    MAX_SMOKE,
    MAX_FLAME,
    MAX_OCCUPANCY
)


class SensorFusion:


    def normalize(self, value, maximum):

        score = (value / maximum) * 100

        if score > 100:
            score = 100

        if score < 0:
            score = 0

        return score


    def calculate(self, sensor):

        temperature_score = self.normalize(
            sensor["temperature"],
            MAX_TEMPERATURE
        )


        smoke_score = self.normalize(
            sensor["smoke"],
            MAX_SMOKE
        )


        flame_score = self.normalize(
            sensor["flame"],
            MAX_FLAME
        )


        occupancy_score = self.normalize(
            sensor["occupancy"],
            MAX_OCCUPANCY
        )


        hazard = (

            temperature_score * TEMPERATURE_WEIGHT +

            smoke_score * SMOKE_WEIGHT +

            flame_score * FLAME_WEIGHT +

            occupancy_score * OCCUPANCY_WEIGHT

        )


        return round(hazard,2)