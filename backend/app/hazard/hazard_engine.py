class HazardEngine:

    @staticmethod
    def update(node):

        score = 0

        score += node.temperature * 0.25

        score += node.smoke * 0.45

        score += node.fire_intensity * 0.30

        node.hazard_score = min(score, 100)

        node.spread_probability = min(

            node.hazard_score * 1.1,

            100

        )