from fastapi import APIRouter

from app.state.global_state import state_manager
from app.managers.building_manager import BuildingManager


router = APIRouter(
    prefix="/dashboard"
)



@router.get("/state")
def get_state():

    return state_manager.all_nodes()



@router.get("/building")
def get_building():

    building = BuildingManager.get_building()


    if building is None:

        return {
            "error": "Building not loaded"
        }


    return {

        "name": building.name,

        "rooms": [
            vars(room)
            for room in building.rooms.values()
        ],

        "corridors": [
            vars(corridor)
            for corridor in building.corridors.values()
        ],

        "exits": [
            vars(exit)
            for exit in building.exits.values()
        ],

        "connections": building.connections

    }