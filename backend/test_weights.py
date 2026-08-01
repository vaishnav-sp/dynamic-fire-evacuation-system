from app.routing.graph_builder import GraphBuilder
from app.routing.dynamic_graph import DynamicGraph
from app.routing.weight_engine import WeightEngine
from app.config.settings import BUILDING_FILE

building, graph = GraphBuilder(BUILDING_FILE).load()

hazard_map = {
    "R1": {"state": "SAFE"},
    "R2": {
        "hazard_score": 88,
        "predicted_hazard": 84,
        "temperature": 92,
        "smoke": 88,
        "flame": True,
        "occupancy": 0,
        "confidence": 100,
        "state": "CRITICAL"
    },
    "C1": {
        "hazard_score": 58,
        "predicted_hazard": 66,
        "temperature": 62,
        "smoke": 48,
        "flame": False,
        "occupancy": 0,
        "confidence": 100,
        "state": "DANGER"
    }
}

DynamicGraph(graph).update_weights(hazard_map)

for u, v, d in graph.edges(data=True):
    print(f"{u} -> {v} : distance={d['distance']} cost={d['cost']}")