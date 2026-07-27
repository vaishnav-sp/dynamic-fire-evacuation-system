from fastapi import APIRouter

from app.dashboard.dashboard_store import dashboard_state


router = APIRouter(
    prefix="/status",
    tags=["Status"]
)


@router.get("")
def get_status():
    state = dashboard_state.get_state()

    return {
        "nodes": state.get("nodes", {}),
        "evacuation": state.get("evacuation", {}),
    }