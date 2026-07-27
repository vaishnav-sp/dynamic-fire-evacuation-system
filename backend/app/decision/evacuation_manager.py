from app.decision.decision_engine import DecisionEngine
from app.decision.room_blocker import RoomBlocker



class EvacuationManager:


    def __init__(
        self,
        route_manager
    ):

        self.decision_engine = DecisionEngine()

        self.room_blocker = RoomBlocker()

        self.route_manager = route_manager

        self.last_blocked_nodes = []

        self.last_decision = {}



    def update(
        self,
        hazard_map
    ):


        decision = self.decision_engine.evaluate(
            hazard_map
        )


        blocked = self.room_blocker.get_blocked_nodes(
            hazard_map
        )


        # Store latest information

        self.last_blocked_nodes = blocked

        self.last_decision = decision



        return {


            "decision": decision,


            "blocked_nodes": blocked

        }



    def get_route(
        self,
        start,
        exits,
        hazard_map
    ):


        # Update graph weights

        self.route_manager.update(
            hazard_map
        )



        # Calculate blocked nodes

        blocked_nodes = self.room_blocker.get_blocked_nodes(
            hazard_map
        )



        route = self.route_manager.calculate_route(

            start,

            exits,

            blocked_nodes

        )



        return route



    def get_status(self):


        return {


            "decision":
                self.last_decision,


            "blocked_nodes":
                self.last_blocked_nodes

        }