import random
import time

from app.config.settings import BUILDING_FILE

from app.routing.graph_builder import GraphBuilder

from app.simulation.fire_profiles import FireProfile
from app.simulation.occupancy_simulator import OccupancySimulator
from app.simulation.scenario_manager import ScenarioManager
from app.simulation.virtual_nodes import VirtualNodes
from app.hazard.fire_engine import FireEngine
from app.hazard.hazard_engine import HazardEngine
from app.hazard.simulation_clock import SimulationClock
from app.hazard.propagation_engine import PropagationEngine
from app.prediction.fire_predictor import FirePredictor

class Simulator:

    def __init__(self):

        building, _ = GraphBuilder(BUILDING_FILE).load()

        self.building = building

        self.nodes = VirtualNodes()

        self.scenario = ScenarioManager()

        self.scenario.initialize(building)

        self.scenario.ignite("R2")

        self.occupancy = OccupancySimulator()

        self.occupancy.initialize(building)

        self.clock = SimulationClock()

        self.propagation = PropagationEngine(

            self.building,

            self.scenario

        )

        self.predictor = FirePredictor()

        self.virtual_rooms = [

            "R2",
            "R3",
            "R4",
            "R5",
            "C2"
        ]

    def choose_profile(self, node):

        state = self.scenario.get(node)

        return {

            "temperature": state.temperature,

            "smoke": state.smoke,

            "flame": state.flame

        }

    def step(self):

        self.clock.update()

        self.occupancy.update()

        for node_id in self.virtual_rooms:

            node = self.scenario.get(node_id)

            FireEngine.update(node)

            HazardEngine.update(node)

            self.predictor.update(
                node_id,
                node.hazard_score
            )

            prediction = self.predictor.predict(node_id)

            profile = {

                "temperature": node.temperature,

                "smoke": node.smoke,

                "flame": node.flame,

                "hazard": node.hazard_score,

                "prediction": prediction

            }

            self.nodes.publish(

                node_id,

                "VIRTUAL",

                profile,

                self.occupancy.get(node_id)

            )

            print(
                f"[{self.clock.time():03}] "
                f"{node.node_id:<3} "
                f"{'🔥' if node.flame else ' '} "
                f"T={node.temperature:6.1f} "
                f"S={node.smoke:6.1f} "
                f"F={node.fire_intensity:6.1f} "
                f"H={node.hazard_score:6.1f}"
            )

        self.propagation.update()

    def run(self):

        print("Simulator Started")

        while True:

            self.step()

            time.sleep(1)