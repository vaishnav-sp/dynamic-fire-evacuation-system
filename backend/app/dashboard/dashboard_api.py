from fastapi import APIRouter

from app.dashboard.dashboard_store import dashboard_state


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)



@router.get("/state")
def get_dashboard_state():

    return dashboard_state.get_state()



@router.get("/health")
def dashboard_health():

    return {

        "status":"ONLINE",

        "service":"Fire Commander Dashboard"

    }

@router.post("/start/{node_id}")
def set_start(node_id: str):

    dashboard_state.set_start_node(node_id)

    return {
        "start": node_id,
        "status": "UPDATED"
    }