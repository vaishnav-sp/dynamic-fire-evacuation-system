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