from app.decision.decision_engine import DecisionEngine
from app.decision.room_blocker import RoomBlocker


hazard_map = {

    "R2":{
        "hazard":85,
        "prediction_score":100
    },

    "R3":{
        "hazard":10,
        "prediction_score":5
    }

}


decision = DecisionEngine()

blocker = RoomBlocker()


print(
    decision.evaluate(
        hazard_map
    )
)


print(
    blocker.get_blocked_nodes(
        hazard_map
    )
)