class ActuatorManager:


    def generate_commands(
        self,
        evacuation_status
    ):


        commands = {}


        blocked = evacuation_status.get(
            "blocked_nodes",
            []
        )


        decision = evacuation_status.get(
            "decision",
            {}
        )


        critical_nodes = decision.get(
            "critical_nodes",
            []
        )


        for node in blocked:


            commands[node] = {

                "led":
                    "RED_PULSE",

                "buzzer":
                    "CRITICAL"

            }



        for node in evacuation_status.get(
            "route",
            {}
        ).get(
            "path",
            []
        ):


            if node in commands:

                continue


            commands[node] = {

                "led":
                    "GREEN_CHASE",

                "buzzer":
                    "NORMAL"

            }



        for node in critical_nodes:


            commands[node] = {

                "led":
                    "RED_PULSE",

                "buzzer":
                    "EVACUATE"

            }



        if not commands:


            return {

                "system":
                    "WAITING"

            }



        return commands