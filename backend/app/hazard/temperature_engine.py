class TemperatureEngine:

    @staticmethod
    def update(state):

        if state.flame:

            state.temperature += 4

            state.temperature = min(
                state.temperature,
                300
            )

        else:

            if state.temperature > 25:

                state.temperature -= 0.3