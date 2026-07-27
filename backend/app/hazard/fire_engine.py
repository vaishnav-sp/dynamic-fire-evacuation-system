class FireEngine:


    @staticmethod
    def ignite(node):

        node.flame = max(
            node.flame,
            20
        )

        node.temperature = max(
            node.temperature,
            60
        )

        node.smoke = max(
            node.smoke,
            20
        )

        node.fire_intensity = max(
            getattr(node, "fire_intensity", 0),
            30
        )



    @staticmethod
    def update(node):


        if node.flame <= 0:

            return



        intensity = getattr(
            node,
            "fire_intensity",
            0
        )


        # Faster growth as fire increases

        node.temperature += (
            2 + intensity * 0.05
        )


        node.smoke += (
            1 + intensity * 0.03
        )


        node.flame += (
            0.5 + intensity * 0.02
        )


        node.fire_intensity += 2



        node.temperature = min(
            node.temperature,
            350
        )


        node.smoke = min(
            node.smoke,
            100
        )


        node.flame = min(
            node.flame,
            100
        )


        node.fire_intensity = min(
            node.fire_intensity,
            100
        )