import time
import threading
import json

from app.hazard.fire_engine import FireEngine
from app.hazard.propagation_engine import PropagationEngine


class ScenarioEngine:


    def __init__(
        self,
        mqtt_client,
        building=None,
        scenario=None
    ):

        self.client = mqtt_client

        self.building = building

        self.scenario = scenario



    def publish(
        self,
        node
    ):


        payload = {

            "node_id":
                node.node_id,

            "node_type":
                "VIRTUAL",

            "temperature":
                node.temperature,

            "smoke":
                node.smoke,

            "flame":
                bool(node.flame),

            "fire_intensity":
                getattr(
                    node,
                    "fire_intensity",
                    0
                ),

            "occupancy":
                node.occupancy,

            "health":
                "ONLINE",

            "confidence":
                100,

            "timestamp":
                time.time()
        }



        self.client.publish(

            f"building/node/{node.node_id}",

            json.dumps(payload)

        )



        print(
            "Spread Update:",
            payload
        )





    def run_spread(
        self,
        node_id
    ):


        if self.scenario is None:

            print(
                "No scenario manager connected"
            )

            return



        source = self.scenario.get(
            node_id
        )


        if source is None:

            return



        FireEngine.ignite(
            source
        )



        propagation = PropagationEngine(

            self.building,

            self.scenario

        )



        for _ in range(20):


            propagation.update()



            for node in self.scenario.all_nodes():

                self.publish(
                    node
                )



            time.sleep(5)






    def flashover(
        self,
        node_id
    ):


        thread = threading.Thread(

            target=self.run_spread,

            args=(node_id,)

        )


        thread.start()