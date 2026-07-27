from fastapi import APIRouter

from app.dashboard.dashboard_store import dashboard_state


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)

@router.post("/flashover/{node_id}")
def trigger_flashover(node_id: str):
    dashboard_state.apply_scenario(node_id, "FLASHOVER")

    return {
        "scenario": "FLASHOVER",
        "node": node_id,
        "status": "APPLIED",
    }






@router.post("/smoldering/{node_id}")
def trigger_smolder(node_id: str):
    dashboard_state.apply_scenario(node_id, "SMOLDERING")

    return {
        "scenario": "SMOLDERING",
        "node": node_id,
        "status": "APPLIED",
    }


@router.post("/reset")
def reset_simulation():
    dashboard_state.reset_state()

    return {
        "scenario": "RESET",
        "status": "APPLIED",
    }