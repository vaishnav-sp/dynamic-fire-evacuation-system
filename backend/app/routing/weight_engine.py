class WeightEngine:

    # -----------------------------
    # Tunable Weights
    # -----------------------------

    DISTANCE_WEIGHT = 1.0

    HAZARD_WEIGHT = 2.0

    PREDICTION_WEIGHT = 3.0

    SMOKE_WEIGHT = 2.0

    TEMPERATURE_WEIGHT = 0.5

    OCCUPANCY_WEIGHT = 2.0

    CONFIDENCE_WEIGHT = 0.2

    STATE_PENALTY = {
        "SAFE": 0,
        "MODERATE": 40,
        "DANGER": 120,
        "CRITICAL": 100000
    }

    FLAME_PENALTY = 500

    @staticmethod
    def calculate(edge, hazard_map):

        source = hazard_map.get(edge["from"], {})
        target = hazard_map.get(edge["to"], {})

        distance = edge.get("distance", 1)

        # -------------------------
        # Use the WORST endpoint
        # -------------------------

        hazard = max(
            source.get("hazard_score", 0),
            target.get("hazard_score", 0)
        )

        prediction = max(
            source.get("predicted_hazard", 0),
            target.get("predicted_hazard", 0)
        )

        smoke = max(
            source.get("smoke", 0),
            target.get("smoke", 0)
        )

        temperature = max(
            source.get("temperature", 0),
            target.get("temperature", 0)
        )

        occupancy = max(
            source.get("occupancy", 0),
            target.get("occupancy", 0)
        )

        confidence = min(
            source.get("confidence", 100),
            target.get("confidence", 100)
        )

        confidence_penalty = (
            100 - confidence
        ) * WeightEngine.CONFIDENCE_WEIGHT

        # -------------------------
        # State Penalty
        # -------------------------

        state_priority = {
            "SAFE": 0,
            "MODERATE": 1,
            "DANGER": 2,
            "CRITICAL": 3
        }

        source_state = source.get("state", "SAFE")
        target_state = target.get("state", "SAFE")

        state = source_state if state_priority[source_state] >= state_priority[target_state] else target_state

        state_penalty = WeightEngine.STATE_PENALTY.get(state, 0)

        # -------------------------
        # Flame Penalty
        # -------------------------

        flame_penalty = 0

        if source.get("flame", False):
            flame_penalty += WeightEngine.FLAME_PENALTY

        if target.get("flame", False):
            flame_penalty += WeightEngine.FLAME_PENALTY

        # -------------------------
        # Final Cost
        # -------------------------

        cost = (

            distance * WeightEngine.DISTANCE_WEIGHT

            + hazard * WeightEngine.HAZARD_WEIGHT

            + prediction * WeightEngine.PREDICTION_WEIGHT

            + smoke * WeightEngine.SMOKE_WEIGHT

            + temperature * WeightEngine.TEMPERATURE_WEIGHT

            + occupancy * WeightEngine.OCCUPANCY_WEIGHT

            + confidence_penalty

            + state_penalty

            + flame_penalty

        )

        return round(cost, 2)