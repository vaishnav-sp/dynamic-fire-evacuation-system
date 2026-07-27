from app.simulation.scenario_publisher import ScenarioPublisher



if __name__ == "__main__":


    publisher = ScenarioPublisher()


    publisher.run(

        node_id="R4",

        scenario="flashover"

    )