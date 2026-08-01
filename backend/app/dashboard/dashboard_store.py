from copy import deepcopy
import networkx as nx
from app.config.settings import BUILDING_FILE
from app.decision.evacuation_manager import EvacuationManager
from app.routing.graph_builder import GraphBuilder
from app.routing.route_manager import RouteManager


class DashboardState:
    def __init__(self):
        self.real_nodes = {}
        self.virtual_nodes = {}

        self.state = {
            "selected_start": "R1",
            "nodes": {},
            "evacuation": {},
            "routes": {}
        }
        self.route_manager = None
        self.evacuation_manager = None
        self._initialize_default_state()


    def _propagate_fire(self, source_node):

        graph = self.building.graph

        for node_id in self.state["nodes"]:

            try:
                distance = nx.shortest_path_length(
                    graph,
                    source_node,
                    node_id
                )

            except nx.NetworkXNoPath:
                continue

            # --------------------------
            # Base values decay with distance
            # --------------------------

            temperature = max(0, 92 - distance * 22)
            smoke = max(0, 88 - distance * 14)

            # --------------------------
            # Corridors spread smoke
            # but reduce heat
            # --------------------------

            node_type = graph.nodes[node_id]["type"]

            if node_type == "CORRIDOR":

                temperature *= 0.60
                smoke *= 1.15

            # --------------------------
            # Exits stay relatively safe
            # --------------------------

            if node_type == "EXIT":

                temperature *= 0.30
                smoke *= 0.50

            # --------------------------
            # Hazard calculation
            # --------------------------

            hazard = min(
                100,
                temperature * 0.35 +
                smoke * 0.65
            )

            prediction = min(
                100,
                hazard + 8
            )

            if hazard >= 80:
                state = "CRITICAL"

            elif hazard >= 60:
                state = "DANGER"

            elif hazard >= 30:
                state = "MODERATE"

            else:
                state = "SAFE"

            self._update_node(

                node_id,

                round(temperature, 1),

                round(smoke, 1),

                node_id == source_node,

                round(hazard, 1),

                round(prediction, 1),

                state

            )

    def _initialize_default_state(self):
        try:
            building, graph = GraphBuilder(BUILDING_FILE).load()
        except Exception as exc:
            print("Dashboard initialization failed:", exc)
            return

        self.building = building
        self.route_manager = RouteManager(graph)
        self.evacuation_manager = EvacuationManager(self.route_manager)

        nodes = {}
        all_nodes = {
            **building.rooms,
            **building.corridors,
            **building.lobbies
        }

        for node_id, node in all_nodes.items():
            nodes[node_id] = {
                "node_type": getattr(node, "node_type", "VIRTUAL"),
                "temperature": getattr(node, "temperature", 0.0),
                "smoke": getattr(node, "smoke", 0.0),
                "flame": getattr(node, "flame", False),
                "occupancy": getattr(node, "occupancy", 0),
                "hazard_score": getattr(node, "hazard_score", 0.0),
                "predicted_hazard": getattr(node, "predicted_hazard", 0.0),
                "prediction": getattr(node, "prediction", {}),
                "hazard": getattr(node, "hazard_score", 0.0),
                "prediction_score": getattr(node, "predicted_hazard", 0.0),
                "state": getattr(node, "state", "SAFE"),
                "confidence": getattr(node, "confidence", 100.0),
                "sensor_online": getattr(node, "sensor_online", True),
                "last_updated": getattr(node, "last_updated", None),
            }

        self.virtual_nodes = deepcopy(nodes)

        self._merge_nodes()
        self._refresh_evacuation()

    def _normalize_node(self, node_id, node):
        if isinstance(node, dict):
            return {
                "node_type": node.get("node_type", "VIRTUAL"),
                "temperature": node.get("temperature", 0.0),
                "smoke": node.get("smoke", 0.0),
                "flame": bool(node.get("flame", False)),
                "occupancy": node.get("occupancy", 0),
                "hazard_score": node.get("hazard_score", node.get("hazard", 0.0)),
                "predicted_hazard": node.get("predicted_hazard", node.get("prediction_score", 0.0)),
                "prediction": node.get("prediction", {}),
                "hazard": node.get("hazard", node.get("hazard_score", 0.0)),
                "prediction_score": node.get("prediction_score", node.get("predicted_hazard", 0.0)),
                "state": node.get("state", "SAFE"),
                "confidence": node.get("confidence", 100.0),
                "sensor_online": node.get("sensor_online", True),
                "last_updated": node.get("last_updated", None),
            }

        return {
            "node_type": getattr(node, "node_type", "VIRTUAL"),
            "temperature": getattr(node, "temperature", 0.0),
            "smoke": getattr(node, "smoke", 0.0),
            "flame": getattr(node, "flame", False),
            "occupancy": getattr(node, "occupancy", 0),
            "hazard_score": getattr(node, "hazard_score", 0.0),
            "predicted_hazard": getattr(node, "predicted_hazard", 0.0),
            "prediction": getattr(node, "prediction", {}),
            "hazard": getattr(node, "hazard_score", 0.0),
            "prediction_score": getattr(node, "predicted_hazard", 0.0),
            "state": getattr(node, "state", "SAFE"),
            "confidence": getattr(node, "confidence", 100.0),
            "sensor_online": getattr(node, "sensor_online", True),
            "last_updated": getattr(node, "last_updated", None),
        }

    def _merge_nodes(self):
        merged = deepcopy(self.virtual_nodes)

        for node_id, node in self.real_nodes.items():
            merged[node_id] = node

        self.state["nodes"] = merged

    def _refresh_evacuation(self):
        if not self.route_manager or not self.evacuation_manager:
            return

        hazard_map = self.state["nodes"]
        self.route_manager.update(hazard_map)
        evacuation_status = self.evacuation_manager.update(hazard_map)
        blocked_nodes = evacuation_status.get("blocked_nodes", [])
        start_node = self._default_start_node()
        route = self.route_manager.calculate_route(
            start=start_node,
            exits=["E1", "E2"],
            blocked_nodes=blocked_nodes,
        )
        evacuation_status["route"] = route
        evacuation_status["actuator_commands"] = {}
        self.state["evacuation"] = evacuation_status
        self.state["routes"] = {"current": route, "blocked_nodes": blocked_nodes}

    def _default_start_node(self):
        return self.state.get("selected_start", "R1")

    def _get_neighbors(self, node_id):
        if self.building is None:
            return []
        return self.building.get_neighbors(node_id)

    def _update_node(self, node_id, temperature, smoke, flame, hazard, predicted_hazard, state):
        if node_id not in self.state["nodes"]:
            return

        node = self.virtual_nodes[node_id]
        node["temperature"] = temperature
        node["smoke"] = smoke
        node["flame"] = flame
        node["hazard_score"] = hazard
        node["predicted_hazard"] = predicted_hazard
        node["prediction_score"] = predicted_hazard
        node["hazard"] = hazard
        node["state"] = state
        node["confidence"] = 100.0

    def apply_scenario(self, node_id, scenario):

        if not self.state["nodes"]:
            self._initialize_default_state()

        if node_id not in self.state["nodes"]:
            return {
                "status": "NODE_NOT_FOUND",
                "node": node_id
            }

        # Reset everything first

        for node in self.state["nodes"].values():

            node["temperature"] = 0
            node["smoke"] = 0
            node["flame"] = False
            node["hazard_score"] = 0
            node["predicted_hazard"] = 0
            node["prediction_score"] = 0
            node["hazard"] = 0
            node["state"] = "SAFE"

        if scenario == "FLASHOVER":

            self._propagate_fire(node_id)

        else:

            self._propagate_fire(node_id)

            # Smoldering is weaker

            for node in self.state["nodes"].values():

                node["temperature"] *= 0.65
                node["smoke"] *= 0.75
                node["hazard_score"] *= 0.70
                node["hazard"] = node["hazard_score"]

        self._merge_nodes()
        self._refresh_evacuation()

        return self.state

    def reset_state(self):

        self.real_nodes.clear()
        self.virtual_nodes.clear()

        self._initialize_default_state()

        return self.state

    def update_nodes(self, nodes):

        for node_id, node in nodes.items():
            self.real_nodes[node_id] = self._normalize_node(node_id, node)

        self._merge_nodes()
        self._refresh_evacuation()

    def update_evacuation(self, data):
        self.state["evacuation"] = data

    def update_routes(self, data):
        self.state["routes"] = data

    def get_state(self):
        return deepcopy(self.state)

    def set_start_node(self, node_id):

        if node_id not in self.state["nodes"]:
            return

        self.state["selected_start"] = node_id
        self._refresh_evacuation()


dashboard_state = DashboardState()