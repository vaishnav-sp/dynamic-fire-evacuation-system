import json
import time
import paho.mqtt.client as mqtt

from app.simulation.scenario_engine import ScenarioEngine



class ScenarioRunner:


    def __init__(self):

        self.client = mqtt.Client()

        self.engine = ScenarioEngine()



    def start(
        self,
        node,
        scenario,
        duration=30
    ):


        self.client.connect(
            "localhost",
            1883
        )


        self.client.loop_start()


        start_time = time.time()


        while True:


            elapsed = int(
                time.time()-start_time
            )


            if elapsed > duration:

                break



            payload = self.engine.generate(

                scenario,

                node,

                elapsed

            )



            topic = (
                f"building/node/{node}"
            )


            self.client.publish(

                topic,

                json.dumps(payload)

            )


            print(
                "Injected:",
                payload
            )


            time.sleep(1)



        self.client.loop_stop()