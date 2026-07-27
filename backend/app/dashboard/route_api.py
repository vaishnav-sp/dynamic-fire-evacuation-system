from fastapi import APIRouter

from app.dashboard.dashboard_store import dashboard_state


router = APIRouter(
    prefix="/route",
    tags=["Route"]
)



@router.get("/comparison")
def route_comparison():

    state = dashboard_state.get_state()


    evacuation = state.get(
        "evacuation",
        {}
    )


    route = evacuation.get(
        "route",
        {}
    )


    if not route:

        return {

            "status":
                "NO_ROUTE",

            "message":
                "No evacuation route calculated"

        }



    safest = route



    # Temporary shortest calculation
    # RouteManager already has this logic.
    # We expose current result first.


    return {

        "status":
            "ACTIVE",


        "safest_route":
        {

            "path":
                safest.get(
                    "path"
                ),

            "cost":
                safest.get(
                    "cost"
                ),

            "risk":
                "LOW"

        },


        "shortest_route":
        {

            "path":
                safest.get(
                    "path"
                ),

            "distance":
                safest.get(
                    "cost"
                ),

            "risk":
                "UNKNOWN"

        }

    }