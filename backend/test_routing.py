from app.routing.graph_builder import GraphBuilder
from app.routing.route_manager import RouteManager
from app.config.settings import BUILDING_FILE


building, graph = GraphBuilder(
    BUILDING_FILE
).load()


route_manager = RouteManager(graph)



hazard_map = {


"R2":{

"hazard":80,
"occupancy":10,
"confidence":100,
"prediction_score":100

},


"R3":{

"hazard":5,
"occupancy":5,
"confidence":100,
"prediction_score":5

},


"C2":{

"hazard":5,
"occupancy":20,
"confidence":100,
"prediction_score":5

}

}



route_manager.update(
    hazard_map
)



result = route_manager.calculate_route(

    "R2",

    list(building.exits.keys())

)


print(result)