class SmokeEngine:

    @staticmethod
    def update(state):

        if state.flame:

            state.smoke += 5

            state.smoke = min(
                state.smoke,
                100
            )

        else:

            if state.smoke > 0:

                state.smoke -= 0.5