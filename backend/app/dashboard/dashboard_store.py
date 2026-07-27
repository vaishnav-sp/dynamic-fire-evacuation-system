from copy import deepcopy

from app.config.settings import BUILDING_FILE
from app.decision.evacuation_manager import EvacuationManager
from app.routing.graph_builder import GraphBuilder
from app.routing.route_manager import RouteManager


class DashboardState:
    def __init__(self):
        self.state = {"nodes": {}, "evacuation": {}, "routes": {}}
        self.building = None
        self.route_manager = None
        self.evacuation_manager = None
        self._initialize_default_state()

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
        for node_id, node in {**building.rooms, **building.corridors}.items():
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

        self.state["nodes"] = nodes
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
        for candidate in ("R1", "R2", "R3", "C1", "C2"):
            if candidate in self.state["nodes"]:
                return candidate
        return next(iter(self.state["nodes"]), "R1")

    def _get_neighbors(self, node_id):
        if self.building is None:
            return []
        return self.building.get_neighbors(node_id)

    def _update_node(self, node_id, temperature, smoke, flame, hazard, predicted_hazard, state):
        if node_id not in self.state["nodes"]:
            return

        node = self.state["nodes"][node_id]
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
            return {"status": "NODE_NOT_FOUND", "node": node_id}

        if scenario == "FLASHOVER":
            self._update_node(node_id, 92, 88, True, 88, 84, "CRITICAL")
            for neighbor_id in self._get_neighbors(node_id):
                self._update_node(neighbor_id, 62, 48, False, 58, 66, "DANGER")
        else:
            self._update_node(node_id, 68, 54, True, 60, 62, "DANGER")
            for neighbor_id in self._get_neighbors(node_id):
                self._update_node(neighbor_id, 42, 28, False, 34, 42, "MODERATE")

        self._refresh_evacuation()
        return self.state

    def reset_state(self):
        self._initialize_default_state()
        return self.state

    def update_nodes(self, nodes):
        normalized = {}
        for node_id, node in nodes.items():
            normalized[node_id] = self._normalize_node(node_id, node)
        self.state["nodes"] = normalized
        self._refresh_evacuation()

    def update_evacuation(self, data):
        self.state["evacuation"] = data

    def update_routes(self, data):
        self.state["routes"] = data

    def get_state(self):
        return deepcopy(self.state)


dashboard_state = DashboardState()