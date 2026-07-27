import json
import time
import paho.mqtt.client as mqtt

from app.simulation.scenario_engine import ScenarioEngine



class ScenarioPublisher:


    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.connect(
            "localhost",
            1883
        )

        self.engine = ScenarioEngine()



    def run(
        self,
        node_id,
        scenario
    ):


        timeline = self.engine.generate(
            scenario,
            node_id
        )


        for data in timeline:


            topic = (
                f"building/node/{node_id}"
            )


            self.client.publish(

                topic,

                json.dumps(data)

            )


            print(
                "Injected:",
                data
            )


            time.sleep(1)